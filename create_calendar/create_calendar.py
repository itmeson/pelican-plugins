# -*- coding: utf-8 -*-
"""
Create Calendar
===============

This plugin parses the article metadata to find duedate: tags
then compiles the relevant articles into entries in an icalendar file.
"""


from pelican import signals


def test(sender):
    #print "%s initialized !!" % sender
    pass    

def find_due_dates(generator):
    import inspect
    # there simply *has* to be a better way to get the siteurl, but this does work
    a = inspect.getmembers(generator, lambda a:not(inspect.isroutine(a)))
    SITEURL = a[2][1]['settings']['SITEURL']

    assignments = []
    for article in generator.articles:
	if hasattr(article,'duedate'): 
	    assignments.append(article)
	    q = article.summary
    if len(assignments) > 0:
	generate_ical(assignments, generator.output_path, SITEURL)

def generate_ical(assignments, output_path, SITEURL):
    from icalendar import Calendar, Event
    import datetime
    import pytz
 
    cal = Calendar()

    cal.add('prodid', '-//My calendar product//mxm.dk//')
    cal.add('version', '2.0')

    for (count, a) in enumerate(assignments):
        event = Event()
	summary = strip_tags(a.summary).strip()
        event.add('summary', summary)
        date = datetime.datetime.strptime(a.duedate, '%Y-%m-%d')
	date += datetime.timedelta(hours=25)
	description = 'More Info: ' + SITEURL + '/' + a.url + ' DUE: ' + a.duedate
	event.add('dtstart', date)
	event.add('uid', str(count) + 'mbetnel@seattleacademy.mrooms3.net')
	event.add('description', description) 
        cal.add_component(event)

    import os
    f = open(os.path.join(output_path, 'assignments.ics'), 'wb')
    f.write(cal.to_ical())
    f.close()



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
