# 6.00 Problem Set 5
# RSS Feed Filter

import feedparser
import string
import time
from project_util import translate_html
from news_gui import Popup

#-----------------------------------------------------------------------
#
# Problem Set 5

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        summary = translate_html(entry.summary)
        try:
            subject = translate_html(entry.tags[0]['term'])
        except AttributeError:
            subject = ""
        newsStory = NewsStory(guid, title, subject, summary, link)
        ret.append(newsStory)
    return ret

#======================
# Part 1
# Data structure design
#======================

# Problem 1

class NewsStory(object):
    def __init__(self, guid, title, subject, summary, link):
        self.guid = guid
        self.title = title
        self.subject = subject
        self.summary = summary
        self.link = link

    def get_guid(self):
        return self.guid
    def get_title(self):
        return self.title
    def get_subject(self):
        return self.subject
    def get_summary(self):
        return self.summary
    def get_link(self):
        return self.link

#======================
# Part 2
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        raise NotImplementedError

# Whole Word Triggers
# Problems 2-5

class WordTrigger(Trigger):
    def __init__(self, word):
        self.word = word

    def is_word_in(self, text):
        word = self.word.lower()
        text = text.lower()
        for i in string.punctuation:
            text = text.replace(i, ' ')
        text = text.split(' ')
        if word in text:
            return True
        return False

class TitleTrigger(WordTrigger):
    def evaluate(self, story):
        return self.is_word_in(story.get_title())
class SubjectTrigger(WordTrigger):
    def evaluate(self, story):
        return self.is_word_in(story.get_subject())
class SummaryTrigger(WordTrigger):
    def evaluate(self, story):
        return self.is_word_in(story.get_summary())

# Composite Triggers
# Problems 6-8

class NotTrigger(Trigger):
    def __init__(self, other_trigger):
        self.trigger = other_trigger
    def evaluate(self, story):
        return not self.trigger.evaluate(story)

class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    def evaluate(self, story):
        return self.trigger1.evaluate(story) and self.trigger2.evaluate(story)

class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2
    def evaluate(self, story):
        return self.trigger1.evaluate(story) or self.trigger2.evaluate(story)


# Phrase Trigger
# Question 9

class PhraseTrigger(Trigger):
    def __init__(self, phrase):
        self.phrase = ' '.join(phrase)
        print self.phrase
    def evaluate(self, story):
        return self.phrase in story.get_subject() or self.phrase in story.get_title() or self.phrase in story.get_summary()

#======================
# Part 3
# Filtering
#======================

def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory-s.
    Returns only those stories for whom
    a trigger in triggerlist fires.
    """
    selected = []
    for story in stories:
        for trigger in triggerlist:
            if trigger.evaluate(story):
                selected.append(story)
    return selected
        
#======================
# Part 4
# User-Specified Triggers
#======================

def generateTrigger(trigger_dict, trigger_name, trigger_type, trigger_arg):
    if trigger_type == 'SUBJECT':
        trigger = SubjectTrigger(trigger_arg)
    elif trigger_type == 'SUMMARY':
        trigger = SummaryTrigger(trigger_arg)
    elif trigger_type == 'TITLE':
        trigger = TitleTrigger(trigger_arg)
    elif trigger_type == 'PHRASE':
        trigger = PhraseTrigger(trigger_arg)
    elif trigger_type == 'AND':
        trigger = AndTrigger(trigger_dict[trigger_arg[0]], trigger_dict[trigger_arg[1]])
    elif trigger_type == 'OR':
        trigger = OrTrigger(trigger_dict[trigger_arg[0]], trigger_dict[trigger_arg[1]])
    elif trigger_type == 'NOT':
        trigger = NotTrigger(trigger_dict[trigger_name])

    #This stores all of the created triggers; calling is done later by the ADD line(s)
    trigger_dict[trigger_name] = trigger
    
    print trigger_dict

def readTriggerConfig(filename):
    """
    Returns a list of trigger objects
    that correspond to the rules set
    in the file filename
    """
    # Here's some code that we give you
    # to read in the file and eliminate
    # blank lines and comments
    triggerfile = open(filename, "r")
    all_lines = [ line.rstrip() for line in triggerfile.readlines() ]
    lines = []
    for line in all_lines:
        if len(line) == 0 or line[0] == '#':
            continue
        lines.append(line)

    # 'lines' has a list of lines you need to parse
    # Build a set of triggers from it and
    # return the appropriate ones
    trigger_dict = {}
    triggerlist = []
    for line in lines:
        line = line.split(' ')
        if line[0] != 'ADD': 
            if line[1] == 'PHRASE' or line[1] == 'AND' or line[1] == 'OR':
                generateTrigger(trigger_dict, line[0], line[1], line[2:])

            else:
                generateTrigger(trigger_dict, line[0], line[1], line[2])
        else:
            for trig in line[1:]:
                triggerlist.append(trigger_dict[trig])
    return triggerlist
    
import thread

def main_thread(p):
    
    # After implementing readTriggerConfig, uncomment this line 
    triggerlist = readTriggerConfig("triggers.txt")
    print triggerlist

    guidShown = []
    
    while True:
        print "Polling..."

        # Get stories from Google's Top Stories RSS news feed
        stories = process("http://news.google.com/?output=rss")
        # Get stories from Yahoo's Top Stories RSS news feed
        stories.extend(process("http://rss.news.yahoo.com/rss/topstories"))

        # Only select stories we're interested in
        stories = filter_stories(stories, triggerlist)
    
        # Don't print a story if we have already printed it before
        newstories = []
        for story in stories:
            if story.get_guid() not in guidShown:
                newstories.append(story)
        
        for story in newstories:
            guidShown.append(story.get_guid())
            p.newWindow(story)

        print "Sleeping..."
        time.sleep(SLEEPTIME)

SLEEPTIME = 60 #seconds -- how often we poll
if __name__ == '__main__':
    p = Popup()
    thread.start_new_thread(main_thread, (p,))
    p.start()

