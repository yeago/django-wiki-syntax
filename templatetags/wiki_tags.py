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
		string = markdown(string.replace('[[','LBRACK666').replace(']]','RBRACK666')).replace('LBRACK666','[[').replace('RBRACK666',']]')

		content = wikify_string(string)
		if len(content.split("</p>")) == 2 and content.split("</p>")[1] == "":
			content = content.replace("<p>","").replace("</p>","")

		#content = re.sub('(.*?)(?:(?:\r\n\r\n)*$|\r\n\r\n)','<p>%s</p>\r\n' % r'\1' , content)
		return content.replace("[[","").replace("]]","")

@register.tag
def wikify(parser, token):
	tag_name, var = token.split_contents()
	string = template.Variable(var)
	return WikiFormat(string)

