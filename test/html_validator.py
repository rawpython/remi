try:
    from html.parser import HTMLParser
except ImportError:
    from HTMLParser import HTMLParser

class SimpleParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.elements = []

    def handle_starttag(self, tag, attrs):
        self.elements.append((tag, dict(attrs)))

def assertValidHTML(text):
    h = SimpleParser()
    h.feed(text) 
    # throws expections if invalid.
    return True