from flask import jsonify, request
from pbu import list_to_json
from storage.models.dataset import Dataset
from storage.models.production_data import ProductionData
import datetime


def register_endpoints(app, session):

    # extract stores for API endpoints (mongo_example is just for illustration)
    @app.route("/api/get-prod-metrics", methods=["GET"])
    def get_prod_metrics():
        metrics = Dataset.query.filter(name="production").first()
        print(metrics)
        return jsonify(metrics)
    
    @app.route("/api/get-all-metrics", methods=["GET"])
    def get_all_metrics():
        metrics = Dataset.query.all()
        print(metrics)
        return jsonify(list_to_json(metrics))

    @app.route("/api/summarize", methods=["POST"])
    def summarize():
        body = request.get_json()
        print(body)
        data = body["data"]
        time = datetime.datetime.now()
        one_line_summary = "hello"
        paragraph_summary = "hi man"
        new_data_pont = ProductionData(data=data, time=time, one_line_summary=one_line_summary, one_paragraph_summary=paragraph_summary)
        session.add(new_data_pont)
        session.commit()


