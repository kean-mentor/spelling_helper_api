from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema


db = SQLAlchemy()


class Word(db.Model):
    word_id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String(255), unique=True, nullable=False)

    def __repr__(self):
        return self.value

class WordSchema(Schema):
    word_id = fields.Int()
    value = fields.Str()

words_schema = WordSchema()


class ExamData(db.Model):
    exam_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    score = db.Column(db.Integer, default=0, nullable=False)
    questions = db.Column(db.Text, nullable=False)
    answers = db.Column(db.Text, nullable=True)
    closed = db.Column(db.Boolean, default=False, nullable=False)
    
    def __repr__(self):
        return f"Name: {self.name}, Score: {self.score}"

class ExamDataSchema(Schema):
    exam_id = fields.Int()
    name = fields.Str()
    score = fields.Str()
    questions = fields.Str()
    answers = fields.Str()
    closed = fields.Bool()

exam_data_schema = ExamDataSchema()


def populate_db(app):
    created = False

    with app.app_context():
        if len(Word.query.all()) == 0:
            word_list = [
                'lyuk', 'hely', 'folyik', 'boly', 'robaj', 'olaj', 'karaj',
                'duhaj', 'tolvaj', 'ibolya', 'ajtó', 'papagáj', 'vaj',
                'gereblye', 'talaj', 'moly', 'zsindely', 'bagoly', 'fejes',
                'sajt', 'kehely', 'tutaj', 'bojler', 'gólya', 'golyó'
            ]

            for w in word_list:
                word_obj = Word(value=w)

                db.session.add(word_obj)
            db.session.commit()

            created = True

    return created
