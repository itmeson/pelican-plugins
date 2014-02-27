from pelican import signals

def test(sender):
    print "%s initialized !!" % sender

def find_due_dates(generator):
    assignments = []
    for article in generator.articles:
	if hasattr(article,'duedate'): 
	    print article.title, article.url, article.duedate
	    assignments.append(article)
	else:
	    print article.title, "no due date"
    if len(assignments) > 0:
	generate_ical(assignments)

def generate_ical(assignments):
    for a in assignments:
	print a.title, a.url, a.duedate


def register():
    signals.initialized.connect(test)
    signals.article_generator_finalized.connect(find_due_dates)
