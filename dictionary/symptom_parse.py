__author__ = 'Tang'


import json
import signal
from SymptomParser import SymptomParser
from Symptom import Symptom


parser = SymptomParser("symptoms.dict")



def parse(file_path):
    fp = open(file_path)
    diseases = json.load(fp)
    count = 0
    for disease_name in diseases:
        disease = diseases[disease_name]
        print(str(count) + "/" + str(len(diseases)))
        new_symptoms_list = []
        for symptom in disease["Symptoms"]:
            parse_result = parser.parse(symptom)
            while not parse_result:
                print(symptom)
                hand_input = raw_input()
                if hand_input == ":wq":
                    parser.save_dict()
                    exit("Bye")
                parse_result = parser.input_parse(hand_input, symptom)
            new_symptoms_list += parse_result
        count += 1

        disease["Symptoms"] = new_symptoms_list


def signal_handler():
    print("Parse interrupt")
    parser.save_dict()

signal.signal(signal.SIGINT, signal_handler)
parse("data/disease_A")


"""
symptom_list = json.load(open("symptom_list"))
fp = open("disease.data")
data = json.load(fp)
fp.close()
fp = open("disease.data")
modified = json.load(fp)
fp.close()



def match(sentence):
    match_sym = []
    for item in symptom_list:
        if isinstance(item, basestring):
            if item in sentence:
                print("Match " + item)
                match_sym.append(item)
        else:
            find_all = True
            for part in item:
                if part not in sentence:
                    print("Can not match part " +  part)
                    find_all = False
            if find_all:
                match_sym.append(item)

    if not match_sym:
        print(sentence.encode("utf-8"))
        item_input = raw_input("New Item: ")
        if len(item_input) > 0:
            new_items = item_input.split('|')
            for new_item in new_items:
                item_parts = new_item.split(',')
                for part in item_parts:
                    part = part.strip()
                if len(item_parts) > 1:
                    match_sym.append(item_parts)
                    symptom_list.append(item_parts)
                else:
                    match_sym.append(new_item)
                    symptom_list.append(new_item)
    return match_sym

for name, disease in data.iteritems():
    if "Symptoms" in modified[name]:
        modified[name]["Symptoms"] = []
    for symptom in disease["Symptoms"]:
        match_desc = symptom.lower()
        modified[name]["Symptoms"] = match(match_desc)
"""