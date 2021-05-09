from flask_script import Command
from storage.shared import db
from prod_pipeline.metrics import insert_metrics_into_database


class ComputeMetricsCommand(Command):

    def run(self):
        insert_metrics_into_database(db.session)
        db.session.commit()