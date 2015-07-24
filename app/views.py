from flask import render_template, request
from app import app
import json


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/disease/<disease_id>')
def disease_entry(disease_id):
    from model import Session, Disease

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
	
@app.route('/testFemale')
def testFemale():
    return render_template('testFemale.html')
	
@app.route('/testMale')
def testMale():
    return render_template('testMale.html')


# ------------------------------------- Ajax API ------------------------------------------#
@app.route('/api/diseases', methods=['GET'])
def get_diseases_list():
    from model import Session, Disease

    session = Session()
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    tmp_query = session.query(Disease.disease_id, Disease.disease_name).order_by(Disease.disease_name)
    if limit and str(limit).isdigit():
        tmp_query = tmp_query.limit(int(limit))
    if offset and str(offset).isdigit():
        tmp_query = tmp_query.offset(int(offset))
    result = tmp_query.all()
    return json.dumps(result)


@app.route('/api/diseases/<disease_id>')
def get_disease_detail(disease_id):
    from model import Session, Disease\

    session = Session()
    disease = session.query(Disease).filter(Disease.disease_id == disease_id).first()
    return json.dumps(disease.to_dict())

@app.route('/api/service/symptom-match', methods=['POST'])
def symptom_match():
    from model import Symptom, Disease, DiseaseHasSymptom, Session, FullTextSearch, FullTextMode
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
    from model import PubmedGetter, Session
    from bs4 import BeautifulSoup

    session = Session()
    p = PubmedGetter(query)
    p.send()
    return p.extract()