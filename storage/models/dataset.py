from storage.shared import db, GUID


class Dataset(db.Model):
    id = db.Column(GUID(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    avg_length = db.Column(db.Float)
    count = db.Column(db.Integer)
    sentence_count = db.Column(db.Integer)
    num_medical_terms = db.Column(db.Integer)
    most_common_words = db.Column(db.String(2000))
    avg_sentence_length = db.Column(db.Float)
    avg_sentence_variance = db.Column(db.Float)
    





