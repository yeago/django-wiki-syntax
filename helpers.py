import re

from django.conf import settings
from django.db.models.loading import get_model

class WikiException(Exception): # Raised when a particular string is not found in any of the models.
	pass

def wikify(match): # Excepts a regexp match
	wikis = [] # Here we store our wiki model info

	for i in settings.WIKISYNTAX:
		name = i[0]
		modstring = i[1]
		module = __import__(".".join(modstring.split(".")[:-1]))
		for count, string in enumerate(modstring.split('.')):
			if count == 0:
				continue

			module = getattr(module,string)

		module.name = name
		wikis.append(module())

	token, trail = match.groups() # we track the 'trail' because it may be a plural 's' or something useful

	if ':' in token:
		"""
		First we're checking if the text is attempting to find a specific type of object.

		Exmaples:

		[[user:Subsume]]

		[[card:Jack of Hearts]]

		"""
		prefix = token.split(':',1)[0].lower().rstrip()
		name = token.split(':',1)[1].rstrip()
		for wiki in wikis:
			if prefix == wiki.name:
				return wiki.render(name,trail=trail)

	"""
	Now we're going to try a generic match across all our wiki objects.

	Example:

	[[Christopher Walken]]

	[[Studio 54]]
	[[Beverly Hills: 90210]] <-- notice ':' was confused earlier as a wiki prefix name

	[[Cat]]s <-- will try to match 'Cat' but will include the plural 

	[[Cats]] <-- will try to match 'Cats' then 'Cat'

	"""
	for wiki in wikis:
		if getattr(wiki,'prefix_only',None):
			continue

		if wiki.attempt(token):
			return wiki.render(token,trail=trail)

	"""
	We tried everything we could and didn't find anything.

	So we just return the original string
	"""

	return '%s%s' % (token,trail)

class wikify_string(object):
	def __call__(self, string, wiki_cache = None):
		self.wiki_cache = wiki_cache or {} 
		from wikisyntax import fix_unicode
		if string:
			content = re.sub('\[\[([^\]]+?)\]\](.*?)', self.markup_to_links, fix_unicode.fix_unicode(string))
			return content, self.wiki_cache

		return '', self.wiki_cache # quick fix.

	def __new__(cls, string, **kwargs):
		obj = super(wikify_string, cls).__new__(cls)
		return obj(string, **kwargs)

	def markup_to_links(self,match):
		string = match.groups()[0]

		if not string in self.wiki_cache:
			try:
				new_key = wikify(match)
			except WikiException:
				new_key = string

			if not string in self.wiki_cache:
				self.wiki_cache[string] = new_key

		else:
			pass
				
		return self.wiki_cache[string]
