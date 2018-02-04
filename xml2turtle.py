#import xml.etree.ElementTree as ET
import lxml.etree as etree

tree = etree.parse("finalWord.html")
root = tree.getroot()


for cours in root.iter("COURS"):
    print("***")
    semestre = cours.attrib["semestre"]
    intitule = cours.attrib["titre"]

    miscs = []
    for data in cours.iter("span"):
        txt = etree.tostring(data, pretty_print=False).strip()
        if "</span>" in txt:
            index = txt.index("</span>") + 7
            if index != len(txt):
                miscs.append(txt[index:len(txt)])

    CNU = None
    if "." not in miscs[0]:
        CNU = int(miscs[0])
    horaires = []

    for elem in miscs:
        if "h" in elem:
            horaires.append(int(elem[0:1]))
        elif "." in elem:
            ects = float(elem)

    for data in cours.iter("a"):
        if "href" in data.attrib:
            mail = data.attrib["href"]
            if "mailto" in mail:
                mail = mail.replace("mailto:", "")

    for nom in cours.iter("NOM"):
        name = nom.text.split(" ")

    print(intitule, name, mail, ects, horaires, semestre)
    #return intitule, name, mail, ects, horaires, semestre







intitule = "Distributed Optimization and Games"
respo_name = ("Giovanni", "Neglia")
respo_email = "Giovanni.neglia@sophia.inria.fr"
ects = 2.00
horaires = (12, 14, 16)
semestre = 2
resume = "The focus of this course is on networks interconnecting decision making elements, whose"

def getCoursToTurtule(intitule, respo_name, respo_email, ects, horaires, semestre, resume):
    id_cours = intitule.replace(" ", "_")
    id_respo = respo_name[0] + "_" + respo_name[1]

    respo = "SI:" + id_respo + " rdf:type owl:NamedIndividual ,\nSI:Professeur ;\n"
    respo += "SI:Email \"" + respo_email + "\"^^xsd:string ;\n"
    respo += "SI:Nom \"" + respo_name[0] + "\"^^xsd:string ;\n"
    respo += "SI:Prenom \"" + respo_name[1] + "\"^^xsd:string ;\n"

    cours = "SI:" + id_cours + " rdf:type owl:NamedIndividual ,\nSI:Cours ;\n"
    cours += "SI:Responsable SI:" + id_respo + " ;\n"
    cours += "SI:Intitule \"" + intitule + "\"@fr ;\n"
    cours += "SI:ECTS " + str(ects) + " ;\n"
    cours += "SI:Semestre " + str(semestre) + " .\n"

    if horaires:
        cours += "SI:Horaires_Cours " + str(horaires[0]) + " ;\n"
        if len(horaires) > 1:
            cours += "SI:Horaires_Personnel " + str(horaires[1]) + " ;\n"
        if len(horaires) == 3:
            cours += "SI:Horaires_TD " + str(horaires[2]) + " ;\n"
    if resume is not None:
        cours += "SI:Resume \"" + resume + "\"^^xsd:string ;\n"

    return respo, cours

respo, cours = getCoursToTurtule(intitule, respo_name, respo_email, ects, horaires, semestre, resume)
