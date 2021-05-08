from storage.shared import db, GUID
import datetime


class ProductionData(db.Model):
    id = db.Column(GUID(), primary_key=True)
    data = db.Column(db.Text, unique=False, nullable=False)
    time = db.Column(db.DateTime, default=datetime.datetime.now())
    one_line_summary = db.Column(db.Text)
    one_paragraph_summary = db.Column(db.Text)




