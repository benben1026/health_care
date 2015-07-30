from flask import render_template, request, send_from_directory, session
from sqlalchemy import distinct, exc
from app import app
from model import *
import json, copy


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/disease/<disease_id>')
def disease_entry(disease_id):
    disease = db_session.query(Disease).filter(Disease.disease_id == disease_id).first().to_dict()
    db_session.close()
    return render_template('disease.html', disease=disease)
@app.route('/category')
def disease_category():
    return render_template('category.html')

@app.route('/search')
def search():
    return render_template('search.html')
@app.route('/model')
def model():
    return render_template('model.html')
@app.route('/testMale')
def testMale():
    return render_template('testMale.html')
@app.route('/testFemale')
def testFemale():
    return render_template('testFemale.html')

@app.route('/doc/<file_name>')
def document(file_name):
    import os
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "doc")
    return send_from_directory(path, file_name)


# ------------------------------------- User API ----------------------------------------------#
@app.route('/api/user', methods=['POST', 'GET', 'PUT'])
def add_user():
    err = None
    if request.method == "POST":
        inf = request.get_json()
        for field in User.required:
            if field not in inf:
                return json.dumps({"Err": "Required field missing"})
        new_user = User(inf["email"], inf["password"], inf["username"],
                        gender=inf.get("gender", None),
                        age=inf.get("age", None))
        db_session.add(new_user)
        try:
            db_session.commit()
        except exc.SQLAlchemyError as e:
            db_session.rollback()
            err = str(e)
        finally:
            db_session.close()
        return json.dumps({"Err": err})
    if request.method == "GET":
        if "user" in session:
            user_dict = copy.deepcopy(session["user"])
            user_dict.pop("password", None)
            user_dict.pop("id", None)
            return json.dumps(user_dict)
        else:
            return json.dumps({"Err": "No session"})


@app.route('/api/user/<email>')
def check_exist(email):
    return json.dumps({"exist": User.exist(db_session, email)})


@app.route('/api/session', methods=['POST', 'DELETE'])
def authentic():
    if request.method == "POST":
        inf = request.get_json()
        if "email" not in inf or "password" not in inf:
            return "Invalid"
        authentic_user = User.authentic(db_session, inf["email"], inf["password"])
        permanent = False
        if "permanent" in inf:
            permanent = bool(inf["permanent"])
        if permanent:
            session.permanent = True
        if not authentic_user:
            return json.dumps({"Err": "Invalid email or password"})
        session["user"] = authentic_user.to_dict()
        return json.dumps({"Err": None})
    if request.method == 'DELETE':
        if "user" not in session:
            return json.dumps({"Err": "Do not have a session"})
        session.pop("user", None)
        return json.dumps({"Err": None})


# ------------------------------------- Diseases API ------------------------------------------#

@app.route('/api/diseases', methods=['GET', 'POST'])
def get_diseases_list():
    if request.method == "GET":
        limit = request.args.get('limit')
        offset = request.args.get('offset')
        tmp_query = db_session.query(Disease.disease_id, Disease.disease_name).order_by(Disease.disease_name)
        if limit and str(limit).isdigit():
            tmp_query = tmp_query.limit(int(limit))
        if offset and str(offset).isdigit():
            tmp_query = tmp_query.offset(int(offset))
        result = tmp_query.all()
        db_session.close()
        return json.dumps(result)
    elif request.method == "POST":
        ids = request.get_json()
        diseases = db_session.query(Disease).filter(Disease.disease_id.in_(ids)).all()
        rv = {}
        for disease in diseases:
            rv[disease.disease_id] = disease.to_dict()
        db_session.close()
        return json.dumps(rv)


@app.route('/api/diseases/position', methods=["POST"])
def query_by_position():
    query = request.get_json()
    if not query["level1"] or not query["level2"]:
        return json.dumps({"Err": "Level1 and Level2 position required"})

    level1_id = db_session.query(BodyLevel1.id).filter(BodyLevel1.name == query["level1"]).first()[0]
    level2_id = db_session.query(BodyLevel2.id).filter(BodyLevel2.name == query["level2"]).first()[0]
    if not level1_id or not level2_id:
        return json.dumps({"Err": "Incorrect Level1 or Level2 keyword"})
    diseases = db_session.query(Disease.disease_id, Disease.disease_name).filter(Disease.body_part_1 == level1_id, Disease.body_part_2 == level2_id).all()
    rv = []
    for disease in diseases:
        rv.append(disease)
    db_session.close()
    return json.dumps(rv)


@app.route('/api/diseases/<disease_id>')
def get_disease_detail(disease_id):

    disease = db_session.query(Disease).filter(Disease.disease_id == disease_id).first()
    rv = disease.to_dict()
    db_session.close()
    return json.dumps(rv)


@app.route('/api/position/level1/<level1_pos>')
def query_level1(level1_pos):

    level1_id = db_session.query(BodyLevel1.id).filter(BodyLevel1.name == level1_pos).first()
    if not level1_id:
        return json.dumps({"Err": "Incorrect Level1 keyword"})
    level1_id = level1_id[0]
    level2s = db_session.query(BodyLevel2.id, BodyLevel2.name).filter(BodyLevel2.upper_level_id == level1_id).all()
    db_session.close()
    return json.dumps(level2s)


@app.route('/api/service/symptom-match', methods=['POST'])
def symptom_match():
    from helper import retrieve_subtitle

    if request.method == "POST":
        match_list = request.get_json()
        fulltext_limit = None
        if not match_list:
            return "No content"

        diseases_matched_count = {}
        keyword_length = len(match_list)
        for keyword in match_list:
            symptoms_matched = set()
            for synonym in keyword:
                symptoms_matched_result = db_session.query(Symptom.symptom_id)\
                    .filter(FullTextSearch(synonym, Symptom)).all()
                for symptom_result_tuple in symptoms_matched_result:
                    symptoms_matched.add(symptom_result_tuple[0])
            diseases_matched = db_session.query(distinct(DiseaseHasSymptom.disease_id))\
                .filter(DiseaseHasSymptom.symptom_id.in_(symptoms_matched))\
                .all()
            for diseases_matched_tuple in diseases_matched:
                disease_id = diseases_matched_tuple[0]
                if disease_id in diseases_matched_count:
                    diseases_matched_count[disease_id] += 1
                else:
                    diseases_matched_count[disease_id] = 1
        # Determine how relevant diseases will be returned
        relevant_factor = 0.5
        relevant_min = keyword_length * relevant_factor
        diseases_matched_result = []
        for disease_id in diseases_matched_count:
            if diseases_matched_count[disease_id] > relevant_min:
                diseases_matched_result.append(disease_id)
        # Get description of theses diseases
        diseases_matched_result_tuples = db_session.query(Disease.disease_id, Disease.disease_name, Disease.description).\
            filter(Disease.disease_id.in_(diseases_matched_result)).all()
        rv = []
        for disease_tuple in diseases_matched_result_tuples:
            rv.append({"id": disease_tuple[0],
                       "name": disease_tuple[1],
                       "description": retrieve_subtitle(disease_tuple[2])["Description"],
                       "relevance": diseases_matched_count[disease_tuple[0]]})
        db_session.close()
        return json.dumps(rv)


@app.route('/api/service/search-synonym/<query>')
def search_synonym(query):

    p = PubmedGetter(query)
    p.send()
    db_session.close()
    return p.extract()


