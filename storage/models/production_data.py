from storage.shared import db
import datetime
import uuid


class ProductionData(db.Model):
    id = db.Column(db.String(100), primary_key=True, default=lambda: str(uuid.uuid4()))
    data = db.Column(db.Text, unique=False, nullable=False)
    time = db.Column(db.DateTime, default=datetime.datetime.now)
    one_line_summary = db.Column(db.Text)
    one_paragraph_summary = db.Column(db.Text)




