# coding: utf8
# import lxml.etree as etree
import xml.etree.ElementTree as etree
import re
import json

tree = etree.parse("finalWord.html")
root = tree.getroot()

with open("classes", "r") as f:
    classes = json.load(f)


def getCoursToTurtule(turtule, class_cours, intitule, respo_name, respo_email, ects, horaires, semestre, resume):
    id_cours = intitule.replace(" ", "_").replace("'", "")
    id_cours = re.sub('[^A-Za-z0-9-_]+', '', id_cours)
    id_respo = respo_name[0] + "_" + respo_name[1]
    id_respo = re.sub('[^A-Za-z0-9-_]+', '', id_respo)

    respo = "SI:" + id_respo + " rdf:type owl:NamedIndividual , SI:Professeur ;\n"
    if respo_email is not None:
        respo += "\tSI:Email \"" + respo_email + "\"^^xsd:string ;\n"
    respo += "\tSI:Nom \"" + respo_name[0] + "\"^^xsd:string ;\n"
    respo += "\tSI:Prenom \"" + respo_name[1] + "\"^^xsd:string .\n\n"

    cours = "SI:" + id_cours + " rdf:type owl:NamedIndividual , " + class_cours + " ;\n"
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


def getClass(intitule, resume):
    if resume is None:
        txt = intitule
    else:
        txt = (intitule + " ") * 5 + resume

    txt = txt.strip().lower().encode('ascii', 'ignore') \
        .decode('utf8').split(" ")
    txt = set(txt)

    all_keys = []

    for key, value in classes.items():
        if len(value) == 1:
            if value[0] in txt:
                all_keys.append(key)
        else:
            intervals = txt.intersection(set(value))
            if intervals:
                all_keys.append(key)

    if all_keys:
        all_k = str(all_keys).replace(
            "[", "").replace("]", "").replace("'", "")
        return all_k
    return "SI:Cours"


def make_cours(turtule, cours):
    semestre = cours.attrib["semestre"]
    intitule = cours.attrib["titre"]

    all_horaires = ['Cours', 'TD', 'TP', 'Travail Personnel']
    miscs = []
    for data in cours.iter("span"):
        txt = str(etree.tostring(data)).strip()
        if "</span>" in txt:
            index = txt.index("</span>") + 7
            if index != len(txt):
                miscs.append(txt[index:len(txt)])

    horaires = []
    for elem in miscs:
        elem1 = elem.replace("'", "").replace("\\n", "").strip()
        if "h" in elem:
            elem1 = elem1.replace("h", "")
            horaires.append(int(elem1))
        elif "." in elem:
            ects = float(elem1)

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
        if text.attrib['label'] == 'Résumé':
            resume = text.text

    for description in cours.iter("ul"):
        if "label" in description.attrib:
            for par in description:
                pass

    class_cours = getClass(intitule, resume)

    # print(intitule, name, mail, ects, horaires, semestre)
    getCoursToTurtule(turtule, class_cours, intitule, name, mail,
                      ects, horaires, semestre, resume)


turtule = dict()
for cours in root.iter("COURS"):
    make_cours(turtule, cours)

# str_base = open("base.ttl", "rb").read()
with open("data.rdf", "wb") as f:
    # f.write(str_base)
    for key, value in turtule.items():
        f.write(value.encode("utf-8"))
