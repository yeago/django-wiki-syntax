import re
from django import template

from wikisyntax.helpers import wikify_string

register = template.Library()

class WikiFormat(template.Node):
	def __init__(self, string):
		self.string = string

	def render(self, context):
		string = self.string.resolve(context)
		self.context = context
		from django.contrib.markup.templatetags.markup import markdown
		string = markdown(string.replace('[[','LBRACK666').replace(']]','RBRACK666'))
		string = string.replace('LBRACK666','[[').replace('RBRACK666',']]')
		single_line_pattern = "<p>([^\n]+)\n</p>"
		single_line_result = re.match(single_line_pattern,string,re.MULTILINE)
		"""
		if single_line_result:
			string = single_line_result.groups(0)[0]
		"""

		"""
		As we're processesing a template with this templatetag, we don't want to re-query already-known
		values. We store them in the context so we don't have to retrieve them again
		"""
		if not hasattr(self,'cache'):
			self.cache = {}

		context_variable = 'unlikely_variable_name_for_wiki_syntax_cache'
		if not context_variable in context.render_context:
			context.render_context[context_variable] = {}

		content, wiki_cache = wikify_string(string,wiki_cache=context.get(context_variable))
		context.render_context[context_variable].update(wiki_cache)

		#content = re.sub('(.*?)(?:(?:\r\n\r\n)*$|\r\n\r\n)','<p>%s</p>\r\n' % r'\1' , content)
		return content.replace("[[","").replace("]]","")

@register.tag
def wikify(parser, token):
	tag_name, var = token.split_contents()
	string = template.Variable(var)
	return WikiFormat(string)

