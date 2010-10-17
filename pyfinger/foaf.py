import pyfinger.fingerurl
import getpass, pwd, os
try:
    from json import dumps
except ImportError:
    from simplejson import dumps
from ordf.command import Command
from ordf.graph import Graph
from ordf.namespace import RDF, FOAF
from ordf.term import URIRef

def serialize_thimbl(g, uri=None):
    if uri is None: uri = g.identifier
    thimbl = { 
        "properties": {},
        "following": [],
        }

    assert g.one((uri, RDF.type, FOAF.Document)), "%s is not a foaf:Document" % uri
    _s, _p, person = g.one((uri, FOAF.primaryTopic, None))

    _s, _p, name = g.one((person, FOAF.name, None))
    thimbl["name"] = name

    def getprop(s, p):
        try:
            _s, _p, o = g.one((s, p, None))
            return o
        except TypeError:
            pass

    email = getprop(person, FOAF.mbox)
    if email is not None:
        thimbl["properties"]["email"] = email
    email_sha1sum = getprop(person, FOAF.mbox_sha1sum)
    if email_sha1sum is not None:
        thimbl["properties"]["email_sha1sum"] = email_sha1sum

    website = getprop(person, FOAF.homepage)
    if website is None:
        website = getprop(person, FOAF.page)
    if website is not None:
        thimbl["properties"]["website"] = website

    for knows in g.distinct_objects(person, FOAF.knows):
        friend = {}
        mbox = getprop(knows, FOAF.mbox)
        if mbox is not None:
            friend["address"] = mbox
        nick = getprop(knows, FOAF.nick)
        if nick is not None:
            friend["nick"] = nick
        friend["seeAlso"] = [ knows ]

        thimbl["following"].append(friend)

    return dumps(thimbl, indent=4)

class Thimbl(Command):
    parser = Command.StandardParser()
    parser.add_option("-f", "--format", 
                      dest="format",
                      default="thimbl",
                      help="Serialise the results in the given format, thimbl (default), "
                      "xml, n3, nt, etc")
    def parse_config(self):
        self.config = {}
    def setup_handler(self):
        pass
    def get_uri(self):
        who = self.args[0]
        user, host = who.split("@", 1)
        if not user.endswith(".foaf"):
            user += ".foaf"
        uri = "finger://%s/%s" % (host, user)
        return URIRef(uri)

    def command(self):
        uri = self.get_uri()
        g = Graph(identifier=uri)
        g.parse(uri, format="n3")

        if self.options.format == "thimbl":
            print serialize_thimbl(g)
        else:
            print g.serialize(format=self.options.format)


def thimbl():
    t = Thimbl()
    t.command()
    
