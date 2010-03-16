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
		string = markdown(string)

		"""
		As we're processesing a template with this templatetag, we don't want to re-query already-known
		values. We store them in the context so we don't have to retrieve them again
		"""

		context_variable = 'unlikely_variable_name_for_wiki_syntax_cache'
		if not context_variable in context:
			context[context_variable] = {}

		content, wiki_cache = wikify_string(string,wiki_cache=context.get(context_variable))
		context.get(context_variable).update(wiki_cache)

		content = re.sub('(.*?)(?:(?:\r\n\r\n)*$|\r\n\r\n)','<p>%s</p>\r\n' % r'\1' , content)
		return content.replace("[[","").replace("]]","")

@register.tag
def wikify(parser, token):
	tag_name, var = token.split_contents()
	string = template.Variable(var)
	return WikiFormat(string)

