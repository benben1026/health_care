from flask import render_template, request
from app import app
import json

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/diseases', methods=['GET'])
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

@app.route('/diseases/<disease_id>')
def get_disease_detail(disease_id):
    from model import Session, Disease
    session = Session()
    disease = session.query(Disease).filter(Disease.disease_id == disease_id).first()
    return json.dumps(disease.to_dict())

