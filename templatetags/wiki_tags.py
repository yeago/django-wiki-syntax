import re
from django import template

from wikisyntax.helpers import wikify_string

register = template.Library()

class WikiFormat(template.Node):
	def __init__(self, string):
		self.string = string

	def build_string(self, context):
		return self.string.resolve(context)

	def process_string(self, string):
		string = string.replace('[[','LBRACK666').replace(']]','RBRACK666').replace('LBRACK666','[[').replace('RBRACK666',']]')
		string = wikify_string(string)
		if len(string.split("</p>")) == 2 and string.split("</p>")[1] == "":
			string = string.replace("<p>","").replace("</p>","")

		return string

	def render(self, context):
		string = self.build_string(context)
		from django.contrib.markup.templatetags.markup import markdown
		string = self.process_string(string)

		#content = re.sub('(.*?)(?:(?:\r\n\r\n)*$|\r\n\r\n)','<p>%s</p>\r\n' % r'\1' , content)
		return string.replace("[[","").replace("]]","")

class WikiBlockFormat(WikiFormat):
	def build_string(self,context):
		return self.string.render(context)

@register.tag
def wikify(parser, token):
	tag_name, var = token.split_contents()
	string = template.Variable(var)
	return WikiFormat(string)

"""
Wouldn't really use the below because of its conflict with markdown's [link] (text)
"""

@register.tag
def wikiblock(parser, token):
	nodelist = parser.parse(('endwikiblock',))
	parser.delete_first_token()
	return WikiBlockFormat(nodelist)
