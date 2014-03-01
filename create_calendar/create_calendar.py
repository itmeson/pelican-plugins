# -*- coding: utf-8 -*-
"""
Create Calendar
===============

This plugin parses the article metadata to find duedate: tags
then compiles the relevant articles into entries in an icalendar file.
"""


from pelican import signals


def test(sender):
    print "%s initialized !!" % sender

def find_due_dates(generator):
    assignments = []
    for article in generator.articles:
	if hasattr(article,'duedate'): 
	    print article.title, article.url, article.duedate, article.summary
	    assignments.append(article)
	    q = article.summary
	
    if len(assignments) > 0:
	generate_ical(assignments, generator.output_path)

def generate_ical(assignments, output_path):
    from icalendar import Calendar, Event
    import datetime
    import pytz

    cal = Calendar()
 
    cal.add('prodid', '-//My calendar product//mxm.dk//')
    cal.add('version', '2.0')

    for a in assignments:
        event = Event()
	summary = strip_tags(a.summary).strip()
        event.add('summary', summary)
        date = datetime.datetime.strptime(a.duedate, '%Y-%m-%d')
        event.add('dtstart', date)

        cal.add_component(event)

    import os
    f = open(os.path.join(output_path, 'assignments.ics'), 'wb')
    f.write(cal.to_ical())
    f.close()

    for a in assignments:
	print a.title, a.url, a.duedate


from HTMLParser import HTMLParser

class MLStripper(HTMLParser):
    """From stackoverflow: http://stackoverflow.com/questions/753052/strip-html-from-strings-in-python"""
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def register():
    signals.initialized.connect(test)
    signals.article_generator_finalized.connect(find_due_dates)
