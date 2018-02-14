import rdflib
import re


class Sparql2html:
    def __init__(self, query):
        self.query = query
        self.g = rdflib.Graph()
        self.g.parse("..\..\CoursTurtulMC_All_FixedSoFar.owl.xml.rdf",
                     format="application/rdf+xml")

    def execute(self):
        qres = self.g.query(self.query)
        html = "<table class=\"table\">\n<thead>\n<tr>"
        split_q = self.query.split(" ")
        for elem in split_q:
            if elem[0] == '?':
                html += "\n<th>" + elem[1:] + "</th>"
        html += "\n</tr>\n</thead>\n<tbody>"
        for row in qres:
            html += "\n<tr>"
            for elem in row:
                el = elem.replace("_", " ")
                if "#" in el:
                    ind = el.index("#")
                    el = el[ind + 1:]
                html += "\n<th>" + el + "</th>"
            html += "</tr>"
        html += "\n</tbody>\n</table>"
        return html
