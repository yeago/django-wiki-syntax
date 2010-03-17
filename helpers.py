import re

from django.conf import settings
from django.db.models.loading import get_model

class WikiException(Exception): # Raised when a particular string is not found in any of the models.
	pass

class WikiMatch(object): # placeholder object for syntax convenience below.
	def render(self,obj,display=None,trail=None):
		if hasattr(obj,'wiki_render'):
			return '%s%s' % (obj.wiki_render(display=display),trail or '')
		return '<a href="%s">%s</a>%s' % (obj.get_absolute_url(),display or obj,trail or '')

def wikify(match): # Excepts a regexp match
	wikis = [] # Here we store our wiki model info
	for i in settings.WIKISYNTAX_MODELS:
		new_wiki = WikiMatch()
		new_wiki.modelname = i[0]
		new_wiki.fields = i[1]
		new_wiki.model = get_model(*i[0].split('.'))
		new_wiki.prefix = new_wiki.model._meta.verbose_name.replace(' ','-')
		try:
			new_wiki.render = i[2]
		except IndexError:
			pass

		wikis.append(new_wiki)

	name, trail = match.groups() # we track the 'trail' because it may be a plural 's' or something useful

	"""
	First we're checking if the text is attempting to find a specific type of object.

	Exmaple:

	[[user:Subsume]]

	[[card:Jack of Hearts]]

	"""

	if ':' in name and name.split(':',1)[0].lower().rstrip() in [i.prefix for i in wikis]:
		prefix = name.split(':',1)[0].lower().rstrip()
		token = name.split(':',1)[1].rstrip()

		for wiki in wikis:
			if not prefix == wiki.prefix:
				continue

			"""
			If, after checking all the fields, we don't return a model, we're going to raise
			the exception
			"""

			exceptions = []

			for field in wiki.fields:
				try:
					obj = wiki.objects.get(**{ field: token })
					return wiki.render(obj,trail=trail)
				except wiki.model.DoesNotExist, e:
					exceptions.append(e)
				except wiki.model.MultipleObjectsReturned, e:
					exceptions.append(e)

			for e in exceptions:
				raise e

	"""
	Now we're going to try a generic match across all our models, unlike the former
	case, we don't care about DoesNotExist errors since the user isn't specifically 
	looking for a particular type.

	Example:

	[[Christopher Walken]]

	[[Studio 54]]

	[[Cat]]s <-- will try to match 'Cat' but will include the plural 

	[[Cats]] <-- will try to match 'Cats' then 'Cat'

	"""
	exceptions = []
	for wiki in wikis:
		for field in wiki.fields:
			try:
				return wiki.render(wiki.model.objects.get(**{ field: name}))
			except wiki.model.DoesNotExist:
				if name[-1] == "s":
					try:
						obj = wiki.model.objects.get(**{ field: name[:-1]})
						return wiki.render(obj,display='%ss' % (obj))
					except wiki.model.DoesNotExist:
						pass
					except wiki.model.MultipleObjectsReturned, e:
						exceptions.append(e)

			except wiki.model.MultipleObjectsReturned, e:
				exceptions.append(e)

	for e in exceptions:
		raise e

	raise WikiException

class wikify_string(object):
	def __call__(self, string, wiki_cache = None):
		self.wiki_cache = wiki_cache or {} 
		content = re.sub('\[\[([^\]]+?)\]\](.*?)', self.markup_to_links, string)
		return content, self.wiki_cache

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
