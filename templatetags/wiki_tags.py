import re
from django import template
from django.core.cache import cache

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
		values. We cache them.
		"""
		
		content = wikify_string(string)

		#content = re.sub('(.*?)(?:(?:\r\n\r\n)*$|\r\n\r\n)','<p>%s</p>\r\n' % r'\1' , content)
		return content.replace("[[","").replace("]]","")

@register.tag
def wikify(parser, token):
	tag_name, var = token.split_contents()
	string = template.Variable(var)
	return WikiFormat(string)

