#chapter 8 Apres Beginning Django e-commerce

from YAAS.search.models import SearchTerm
from YAAS.models import Item
from django.db.models import Q
STRIP_WORDS = ['a', 'an', 'and', 'by', 'for', 'from', 'in', 'no', 'not', 'of', 'on', 'or', 'that', 'the', 'to', 'with', 'as', 'at', 'but', 'into', 'like', 'off', 'onto', 'up', 'via']

# store the search text in the database
def store(request, q):
	# if search term is at least three chars long, store in db
	if len(q) > 2:
		term = SearchTerm()
		term.q = q
		term.ip_address = request.META.get('REMOTE_ADDR')
		term.save()

# get Items matching the search text
def items(search_text):
	words = _prepare_words(search_text)
	item = Item.active.all()
	results = {}
	results['items'] = []
	# iterate through keywords
	for word in words:
		items = item.filter(Q(name__icontains=word) |Q(description__icontains=word))
		results['items'] = items
	return results

# strip out common words, limit to 5 words
def _prepare_words(search_text):
	words = search_text.split()
	for common in STRIP_WORDS:
		if common in words:
			words.remove(common)
	return words[0:5]

