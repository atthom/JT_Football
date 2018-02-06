# coding: utf8
import lxml.etree as etree
import re
tree = etree.parse("finalWord.html")
root = tree.getroot()


def getCoursToTurtule(turtule, intitule, respo_name, respo_email, ects, horaires, semestre, resume):
    id_cours = intitule.replace(" ", "_").replace("'", "")
    id_cours = re.sub('[^A-Za-z0-9-_]+', '', id_cours)
    id_respo = respo_name[0] + "_" + respo_name[1]
    id_respo = re.sub('[^A-Za-z0-9-_]+', '', id_respo)

    respo = "SI:" + id_respo + " rdf:type owl:NamedIndividual , SI:Professeur ;\n"
    if respo_email is not None:
        respo += "\tSI:Email \"" + respo_email + "\"^^xsd:string ;\n"
    respo += "\tSI:Nom \"" + respo_name[0] + "\"^^xsd:string ;\n"
    respo += "\tSI:Prenom \"" + respo_name[1] + "\"^^xsd:string .\n\n"

    cours = "SI:" + id_cours + " rdf:type owl:NamedIndividual , SI:Cours ;\n"
    cours += "\tSI:Responsable SI:" + id_respo + " ;\n"
    cours += "\tSI:Intitule \"" + intitule + "\"@fr ;\n"
    cours += "\tSI:ECTS " + str(ects) + " ;\n"

    if horaires:
        cours += "\tSI:Horaires_Cours " + str(horaires[0]) + " ;\n"
        if len(horaires) > 1:
            cours += "\tSI:Horaires_Personnel " + str(horaires[1]) + " ;\n"
        if len(horaires) == 3:
            cours += "\tSI:Horaires_TD " + str(horaires[2]) + " ;\n"
    if resume is not None:
        cours += "\tSI:Resume \"" + \
            resume.replace("'", "").replace("\"", "") + "\"^^xsd:string ;\n"

    cours += "\tSI:Semestre " + str(semestre) + " .\n\n"

    if id_respo not in turtule or \
            id_respo in turtule and len(turtule[id_respo]) < len(respo):
        turtule[id_respo] = respo

    if id_cours not in turtule or \
            id_cours in turtule and len(turtule[id_cours]) < len(respo):
        turtule[id_cours] = cours


def make_cours(turtule, cours):
    semestre = cours.attrib["semestre"]
    intitule = cours.attrib["titre"]
    miscs = []
    for data in cours.iter("span"):
        txt = str(etree.tostring(data, pretty_print=False)).strip()
        if "</span>" in txt:
            index = txt.index("</span>") + 7
            if index != len(txt):
                miscs.append(txt[index:len(txt)])

    horaires = []
    for elem in miscs:
        if "h" in elem:
            horaires.append(int(elem[0:1]))
        elif "." in elem:
            ects = float(elem.replace("'", "").strip().replace("\\n", ""))

    for data in cours.iter("a"):
        if "href" in data.attrib:
            mail2 = data.attrib["href"]
            mail = None
            if "mailto" in mail2:
                mail = mail2.replace("mailto:", "")

    for nom in cours.iter("NOM"):
        name = nom.text.split(" ")

    resume = None
    for text in cours.iter("LG"):
        if text.text is not None and len(text.text) > 10:
            resume = text.text

    for description in cours.iter("ul"):
        # print(description.attrib)
        if "label" in description.attrib:
            for par in description:
                pass
                # print(par.text)

    # print(intitule, name, mail, ects, horaires, semestre)
    getCoursToTurtule(turtule, intitule, name, mail,
                      ects, horaires, semestre, resume)


turtule = dict()
for cours in root.iter("COURS"):
    make_cours(turtule, cours)

str_base = open("base.ttl", "rb").read()
with open("data.rdf", "wb") as f:
    # f.write(str_base)
    for key, value in turtule.items():
        f.write(value.encode("utf-8"))
