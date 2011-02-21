import re
from django import template

from wikisyntax.helpers import wikify_string, wikisafe_markdown

register = template.Library()

@register.filter
@template.defaultfilters.stringfilter
def wikimarkdown(value):
	return wikisafe_markdown(value)

class WikiFormat(template.Node):
	def __init__(self, string):
		self.string = string

	def build_string(self, context):
		return self.string.resolve(context)

	def process_string(self, string):
		string = wikisafe_markdown(string)
		string = wikify_string(string)
		if len(string.split("</p>")) == 2 and string.split("</p>")[1] == "":
			string = string.replace("<p>","").replace("</p>","")

		return string

	def render(self, context):
		string = self.build_string(context)
		string = self.process_string(string)

		#content = re.sub('(.*?)(?:(?:\r\n\r\n)*$|\r\n\r\n)','<p>%s</p>\r\n' % r'\1' , content)
		return string.replace("[[","").replace("]]","")

class WikiBlockFormat(WikiFormat):
	def process_string(self,string):
		"""
		Its not generally safe to use markdown on a whole blocktag because the block
		may contain html already and there's no telling how nice it will play.
		"""
		string = wikify_string(string)
		return string

	def build_string(self,context):
		return self.string.render(context)

@register.tag
def wikify(parser, token):
	tag_name, var = token.split_contents()
	string = template.Variable(var)
	return WikiFormat(string)

"""

"""

@register.tag
def wikiblock(parser, token):
	nodelist = parser.parse(('endwikiblock',))
	parser.delete_first_token()
	return WikiBlockFormat(nodelist)
