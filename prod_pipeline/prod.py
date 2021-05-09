from storage.models.production_data import ProductionData
from storage.models.dataset import Dataset
from .metrics import insert_metrics_into_database
import datetime


class ProdOperations:

    def __init__(self, session):
        self.session = session

        # load models

    def summarize(self, text):
        # predict model 1
        # predict model 2
        time = datetime.date.today()
        one_line_summary = "hello"
        one_paragraph_summary = "hi"
        new_data_pont = ProductionData(data=text, time=time, one_line_summary=one_line_summary, one_paragraph_summary=one_paragraph_summary)
        self.session.add(new_data_pont)
        return one_line_summary, one_paragraph_summary

    def get_recent_prod_data(self, num_items=10):
        prod_data = self.session.query(ProductionData).order_by(ProductionData.time).limit(num_items).all()

        return [{"data": prod_datum.data,
                 "time": prod_datum.time ,
                 "one_line_summary": prod_datum.one_line_summary,
                 "one_paragraph_summary": prod_datum.one_paragraph_summary }
                for prod_datum in prod_data]

    def get_daily_prod_data_calls(self):
        curr_time = datetime.date.today()
        num_calls = self.session.query(ProductionData).filter(ProductionData.time == curr_time).count()
        print(num_calls)
        return num_calls

    def get_all_metrics(self):
        row2dict = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}
        metrics_prod = row2dict(self.session.query(Dataset).filter_by(name='production').first())
        metrics_train = row2dict(self.session.query(Dataset).filter_by(name='training').first())

        del metrics_prod['id']
        del metrics_prod['name']
        del metrics_train['id']
        del metrics_train['name']

        return [{
            "name": " ".join([word.capitalize() for word in key.split("_")]),
            "training": val,
            "production": metrics_prod[key]
        } for key, val in metrics_train.items()]

    def refresh_metrics(self):

        insert_metrics_into_database(self.session, production_only=True)