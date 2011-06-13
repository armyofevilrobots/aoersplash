"""Feed parser, templater and out-putter"""
import feedparser
import logging
import os.path
import string
import codecs
import datetime
import time

DTPL = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "templates","index.html")

PTPL = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "templates","post.html")

def get_feed_data(feeds, depth, characters):
    """Return an array of date sorted feed entries"""
    entries = []
    for feed in feeds:
        parser = feedparser.parse(feed)
        for entry in parser.entries:
            entry.topurl = parser.channel.link
        entries.extend(parser.entries)
    #I love how tuples can be > or < than each other :)
    def _skey(entry):
        if hasattr(entry,"published_parsed"):
            return time.mktime(entry.published_parsed)
        elif hasattr(entry, "updated_parsed"):
            return time.mktime(entry.updated_parsed)
        else:
            logging.warn("Missing timestamp in post")
            return 0

    return sorted(entries, key = _skey, reverse = True)

class SplashGenerator:
    """Actually generates the output from a variety of template of feeds."""
    def __init__(self, outfile, wtemplate = DTPL, ptemplate = PTPL,
            depth = 5, characters = 1024, feeds = None):

        logging.info("Going to generate %s with the following regions: \n\t%s" ,
                outfile, "\n\t".join(feeds.keys()))
        self.depth = depth
        self.feeds = feeds or []
        self.outfile = outfile
        self.wtemplate = wtemplate
        self.ptemplate = ptemplate
        self.characters = 1024
        for template in (wtemplate, ptemplate):
            if not os.path.exists(template):
                logging.error("Template file %s doesn't exist." , template)
                raise IOError, "Template not found."

    def get_template(self, tplfile):
        """Get the template data and return a string.Template"""
        try:
            fhdl = codecs.open(tplfile, "r", 'utf-8')
            tpl = fhdl.read()
            fhdl.close()
        except IOError, exc:
            logging.error("Failed to open/read %s with %s" % (tplfile, exc))
            raise IOError, "Template not readable."
        return string.Template(tpl)



    def run(self):
        """Spaghetti placeholder"""
        wtemplate = self.get_template(self.wtemplate)
        ptemplate = self.get_template(self.ptemplate)
        feedout = dict()
        for feed in self.feeds:
            logging.debug("Parsing feed %s for location %s", feed, self.feeds[feed])
            posts = []
            posts = get_feed_data(self.feeds[feed], self.depth, self.characters)
            #Fancy!
            data = [dict(post) for post in posts]
            for post in data:
                if len(post['summary']) > self.characters:
                    offset = post['summary'].find(" ", self.characters - 5)
                    post['summary'] = post['summary'][:offset] + " ..."

            try:
                feedout[feed] = "\n\n<!--item-->\n".join((ptemplate.substitute(**dict(post)) for post in data))

            except KeyError, exc:
                logging.error("Failed to find feed item %s", exc)
                raise

        wrapperout = wtemplate.substitute(**feedout)

        fhdl = codecs.open(self.outfile, "w+", 'utf-8')
        fhdl.write(wrapperout)
        fhdl.close()



