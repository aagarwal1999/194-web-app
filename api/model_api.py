from flask import jsonify, request
from pbu import list_to_json
from prod_pipeline.prod import ProdOperations


def register_endpoints(app, session):
    ops = ProdOperations(session)

    @app.route("/api/refresh-prod-calls", methods=["GET"])
    def refresh_prod_calls():
        recent_prod_data = ops.get_recent_prod_data()
        calls = ops.get_daily_prod_data_calls()

        return jsonify({
            "num_daily_api_calls": calls,
            "recent_api_calls": recent_prod_data
        })
    
    @app.route("/api/get-data", methods=["GET"])
    def get_data():
        metric_data = ops.get_all_metrics()
        calls = ops.get_daily_prod_data_calls()
        recent_prod_data = ops.get_recent_prod_data()

        return jsonify({
            "metric_data": metric_data,
            "num_daily_api_calls": calls,
            "recent_api_calls": recent_prod_data
        })

    @app.route("/api/refresh-prod-metrics", methods=["GET"])
    def refresh_prod_metrics():
        ops.refresh_metrics()
        metric_data = ops.get_all_metrics()
        session.commit()
        return jsonify({
            "metric_data": metric_data,
        })

    @app.route("/api/summarize", methods=["POST"])
    def summarize():
        data = request.get_json()
        one_line_summary, one_paragraph_summary = ops.summarize(data)
        calls = ops.get_daily_prod_data_calls()
        recent_prod_data = ops.get_recent_prod_data()
        session.commit()

        return jsonify({
            "one_line_summary": one_line_summary,
            "one_paragraph_summary": one_paragraph_summary,
            "num_daily_api_calls": calls,
            "recent_api_calls": recent_prod_data
        })


