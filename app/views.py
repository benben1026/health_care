from flask import render_template, request
from app import app
from model import *
import json


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/disease/<disease_id>')
def disease_entry(disease_id):

    session = Session()
    disease = session.query(Disease).filter(Disease.disease_id == disease_id).first().to_dict()
    return render_template('disease.html', disease = disease)
@app.route('/category')
def disease_category():
    return render_template('category.html')

@app.route('/search')
def search():
    return render_template('search.html')
@app.route('/model')
def model():
    return render_template('model.html')


# ------------------------------------- Ajax API ------------------------------------------#
@app.route('/api/diseases', methods=['GET', 'POST'])
def get_diseases_list():

    session = Session()
    if request.method == "GET":
        limit = request.args.get('limit')
        offset = request.args.get('offset')
        tmp_query = session.query(Disease.disease_id, Disease.disease_name).order_by(Disease.disease_name)
        if limit and str(limit).isdigit():
            tmp_query = tmp_query.limit(int(limit))
        if offset and str(offset).isdigit():
            tmp_query = tmp_query.offset(int(offset))
        result = tmp_query.all()
        return json.dumps(result)
    elif request.method == "POST":
        ids = request.get_json()
        diseases = session.query(Disease).filter(Disease.disease_id.in_(ids)).all()
        rv = {}
        for disease in diseases:
            rv[disease.disease_id] = disease.to_dict()
        return json.dumps(rv)

@app.route('/api/diseases/position', methods=["POST"])
def query_by_position():
    query = request.get_json()
    if not query["level1"] or not query["level2"]:
        return json.dumps({"Err": "Level1 and Level2 position required"})
    session = Session()
    level1_id = session.query(BodyLevel1.id).filter(BodyLevel1.name == query["level1"]).first()[0]
    level2_id = session.query(BodyLevel2.id).filter(BodyLevel2.name == query["level2"]).first()[0]
    if not level1_id or not level2_id:
        return json.dumps({"Err": "Incorrect Level1 or Level2 keyword"})
    diseases = session.query(Disease.disease_id, Disease.disease_name).filter(Disease.body_part_1 == level1_id, Disease.body_part_2 == level2_id).all()
    rv = []
    for disease in diseases:
        rv.append(disease)
    return json.dumps(rv)


@app.route('/api/diseases/<disease_id>')
def get_disease_detail(disease_id):

    session = Session()
    disease = session.query(Disease).filter(Disease.disease_id == disease_id).first()
    return json.dumps(disease.to_dict())

@app.route('/api/position/level1/<level1_pos>')
def query_level1(level1_pos):
    session = Session()
    level1_id = session.query(BodyLevel1.id).filter(BodyLevel1.name == level1_pos).first()
    if not level1_id:
        return json.dumps({"Err": "Incorrect Level1 keyword"})
    level1_id = level1_id[0]
    level2s = session.query(BodyLevel2.id, BodyLevel2.name).filter(BodyLevel2.upper_level_id == level1_id).all()
    return json.dumps(level2s)



@app.route('/api/service/symptom-match', methods=['POST'])
def symptom_match():
    from sqlalchemy import func, desc
    session = Session()
    if request.method == "POST":
        match_list = request.get_json()
        fulltext_limit = None
        if match_list:
            match_list[0] = "+"+match_list[0]
            fulltext_limit = " +".join(match_list)
        if fulltext_limit:
            symptoms_matched = []
            symptoms_matched_result = session.query(Symptom.symptom_id)\
                .filter(FullTextSearch(fulltext_limit, Symptom, FullTextMode.BOOLEAN)).all()
            for symptom_result_tuple in symptoms_matched_result:
                symptoms_matched.append(symptom_result_tuple[0])
            diseases_matched = session.query(DiseaseHasSymptom.disease_id, func.count(DiseaseHasSymptom.symptom_id).label("rel"))\
                .filter(DiseaseHasSymptom.symptom_id.in_(symptoms_matched)).group_by(DiseaseHasSymptom.disease_id)\
                .order_by(desc("rel")).all()
            diseases_list = {}
            diseases_limit = []

            for diseases_matched_tuple in diseases_matched:
                diseases_limit.append(diseases_matched_tuple[0])
                diseases_list[diseases_matched_tuple[0]] = {"relevance": diseases_matched_tuple[1]}
            diseases_detail = session.query(Disease.disease_id, Disease.disease_name, Disease.description)\
                .filter(Disease.disease_id.in_(diseases_limit)).all()
            for disease_detail in diseases_detail:
                cur = diseases_list[disease_detail[0]]
                cur["name"] = disease_detail[1]
                cur["description"] = disease_detail[2]
            return json.dumps(diseases_list)

@app.route('/api/service/search-synonym/<query>')
def search_synonym(query):
    session = Session()
    p = PubmedGetter(query)
    p.send()
    return p.extract()


