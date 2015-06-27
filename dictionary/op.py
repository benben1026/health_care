__author__ = 'Tang'

from main import parse_raw, filter_disease
import json

total = 0
prevention = 0
treatment = 0
causes = 0
description = 0
symptom = 0
for index in range(65, 91):
    c = chr(index)
    print(c)
    path = "disease_{0}".format(c)
    fp = open(path)
    data = json.load(fp)
    for disease_name in data:
        total += 1
        if "Symptoms" in data[disease_name]:
            symptom += 1
        if "Treatment" in data[disease_name]:
            treatment += 1
        if "Causes" in data[disease_name]:
            causes += 1
        if "Prevention" in data[disease_name]:
            prevention += 1
        if "description" in data[disease_name]:
            description += 1

print("Total: " + str(total))
print("Symptoms: " + str(symptom))
print("Treatment: " + str(treatment))
print("Causes: " + str(causes))
print("Prevention: " + str(prevention))
print("Description: " + str(description))
