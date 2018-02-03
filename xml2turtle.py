import xml.etree.ElementTree as ET

tree = ET.parse("finalWord.html")
root = tree.getroot()

for child in root[0]:
    print(str(child.tag), str(child.attrib))


intitule = "Distributed Optimization and Games"
respo_name = "Giovanni"
respo_surname = "Neglia"
respo_email = "Giovanni.neglia@sophia.inria.fr"
ects = 2.00
horaires = (12, 14, 16)
semestre = 2
resume = "The focus of this course is on networks interconnecting decision making elements, whose"

def getCoursToTurtule(intitule, respo_name, respo_surname, respo_email, ects, horaires, semestre, resume):
    id_cours = intitule.replace(" ", "_")
    id_respo = respo_surname + "_" + respo_name

    respo = "SI:" + id_respo + " rdf:type owl:NamedIndividual ,\nSI:Professeur ;\n"
    respo += "SI:Email \"" + respo_email + "\"^^xsd:string ;\n"
    respo += "SI:Nom \"" + respo_name + "\"^^xsd:string ;\n"
    respo += "SI:Prenom \"" + respo_surname + "\"^^xsd:string ;\n"

    cours = "SI:" + id_cours + " rdf:type owl:NamedIndividual ,\nSI:Cours ;\n"
    cours += "SI:Responsable SI:" + id_respo + " ;\n"
    cours += "SI:ECTS " + str(ects) + " ;\n"
    cours += "SI:Horaires_Cours " + str(horaires[0]) + " ;\n"
    cours += "SI:Horaires_Personnel " + str(horaires[1]) + " ;\n"
    cours += "SI:Horaires_TD " + str(horaires[2]) + " ;\n"
    cours += "SI:Intitule \"" + intitule + "\"@fr ;\n"
    cours += "SI:Resume \"" + resume + "\"^^xsd:string ;\n"
    cours += "SI:Semestre " + str(semestre) + " .\n"

    return respo, cours

respo, cours = getCoursToTurtule(intitule, respo_name, respo_surname, respo_email, ects, horaires, semestre, resume)


print(respo)

print(cours)
