# coding: utf8

import lxml.etree as etree

tree = etree.parse("finalWord.html")
root = tree.getroot()


def getCoursToTurtule(intitule, respo_name, respo_email, ects, horaires, semestre, resume):
    id_cours = intitule.replace(" ", "_").replace("'", "")
    id_respo = respo_name[0] + "_" + respo_name[1]

    respo = "SI:" + id_respo + " rdf:type owl:NamedIndividual , SI:Professeur ;\n"
    if respo_email is not None:
        respo += "\tSI:Email \"" + respo_email + "\"^^xsd:string ;\n"
    respo += "\tSI:Nom \"" + respo_name[0] + "\"^^xsd:string ;\n"
    respo += "\tSI:Prenom \"" + respo_name[1] + "\"^^xsd:string ;\n"

    cours = "SI:" + id_cours + " rdf:type owl:NamedIndividual , SI:Cours ;\n"
    cours += "\tSI:Responsable SI:" + id_respo + " ;\n"
    cours += "\tSI:Intitule \"" + intitule + "\"@fr ;\n"
    cours += "\tSI:ECTS " + str(ects) + " ;\n"
    cours += "\tSI:Semestre " + str(semestre) + " .\n"

    if horaires:
        cours += "\tSI:Horaires_Cours " + str(horaires[0]) + " ;\n"
        if len(horaires) > 1:
            cours += "\tSI:Horaires_Personnel " + str(horaires[1]) + " ;\n"
        if len(horaires) == 3:
            cours += "\tSI:Horaires_TD " + str(horaires[2]) + " ;\n"
    if resume is not None:
        cours += "\tSI:Resume \"" + resume + "\"^^xsd:string ;\n"

    return respo, cours


def make_cours(cours):

    semestre = cours.attrib["semestre"]
    intitule = cours.attrib["titre"]
    miscs = []
    for data in cours.iter("span"):
        txt = str(etree.tostring(data, pretty_print=False)).strip()
        if "</span>" in txt:
            index = txt.index("</span>") + 7
            if index != len(txt):
                miscs.append(txt[index:len(txt)])

    CNU = None
    if "." not in miscs[0] and "'" not in miscs[0]:
        CNU = int(miscs[0])
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

    # print(intitule, name, mail, ects, horaires, semestre)
    return getCoursToTurtule(intitule, name, mail, ects, horaires, semestre, None)


data = ""
for cours in root.iter("COURS"):
    ttl_respo, ttl_cours = make_cours(cours)
    data += ttl_respo + "\n" + ttl_cours + "\n"

open("data.rdf", "wb").write(data.encode("utf-8"))
