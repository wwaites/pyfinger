import urllib2
import pyfinger.fingerurl

def test_finger():
    uri = "finger://river.styx.org/ww"
    fp = urllib2.urlopen(uri)
    data = fp.read()
    fp.close()
    assert "Plan:" in data

def test_finger_port():
    uri = "finger://river.styx.org:79/ww"
    fp = urllib2.urlopen(uri)
    data = fp.read()
    fp.close()
    assert "Plan:" in data

def test_finger_foaf():
    uri = "finger://river.styx.org/ww.foaf"
    from rdflib.graph import Graph
    g = Graph()
    g.parse(uri, format="n3")
    print g.serialize(format="n3")
