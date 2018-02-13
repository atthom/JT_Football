import rdflib


class Sparql2html:
    def __init__(self, query):
        self.query = query
        self.g = rdflib.Graph()
        self.g.parse("..\..\CoursTurtulMC_All_FixedSoFar.owl.xml.rdf",
                     format="application/rdf+xml")

    def execute(self):
        qres = self.g.query(self.query)
        html = "<table>"
        for row in qres:
            html += "\n<tr>" + str(row) + "</tr>"
        html += "\n</table>"
        return html
