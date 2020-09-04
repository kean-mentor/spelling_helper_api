from flask import abort, Blueprint, jsonify, request

import sqlalchemy

from models import db, exam_data_schema, ExamData, words_schema, Word
from utils import check_answers, prepare_questions


bp = Blueprint('api', __name__)


@bp.route('/exam', methods=['GET'])
def get_exam():
    if 'name' not in request.args:
        abort(400)
    if 'total' not in request.args:
        abort(400)

    name = request.args['name']
    total = int(request.args['total'])
    
    words = [word.value for word in Word.query.all()]
    questions = prepare_questions(total, words)

    exam_data = ExamData(name=name, questions=",".join(questions))
    db.session.add(exam_data)
    db.session.commit()

    return jsonify({'id': exam_data.exam_id, 'questions': questions}), 200

@bp.route('/exam/<int:exam_id>', methods=['PUT'])
def check_quiz(exam_id):
    # Invalid request
    if "answers" not in request.json:
        abort(400)

    exam_data = ExamData.query.get(exam_id)
    # Exam not exists
    if not exam_data:
        abort(404)

    # Questions already answered
    if exam_data.closed:
        abort(400)

    questions = exam_data.questions.split(",")
    answers = request.json['answers']
    # Not enough answers
    if len(questions) != len(answers):
        abort(400)

    # FYI: It can be a problem if words are deleted from the db
    # between the GET exam and PUT exam...
    words = [word.value for word in Word.query.all()]
    result = check_answers(questions, answers, words)

    exam_data.answers = ",".join(answers)
    exam_data.score = sum(result)
    exam_data.closed = True
    db.session.commit()

    return exam_data_schema.dump(exam_data), 200


@bp.route('/words', methods=['GET'])
def get_words():
    words = Word.query.all()
    result = [words_schema.dump(word) for word in words]
    return jsonify(result), 200

@bp.route('/words', methods=['POST'])
def add_word():
    if not request.json or not 'word' in request.json:
        abort(400)

    word = request.json['word']
    if 'j' in word or 'ly' in word:
        word_obj = Word(value=word)
        try:
            db.session.add(word_obj)
            db.session.commit()
            return jsonify({'result': 'Created', 'word_id': word_obj.word_id}), 201
        except sqlalchemy.exc.IntegrityError:
            db.session.rollback()
            return jsonify({'result': 'Already exists'}), 409
    else:
        return jsonify({'result': 'Invalid'}), 400

@bp.route('/words/<string:word>', methods=['DELETE'])
def delete_word(word):
    word_obj = Word.query.filter_by(value=word).first()
    if word_obj:
        db.session.delete(word_obj)
        db.session.commit()
        return jsonify({'result': 'Deleted'}), 200
    abort(404)

@bp.route('/words/<int:word_id>', methods=['DELETE'])
def delete_word_by_id(word_id):
    word_obj = Word.query.get(word_id)
    if word_obj:
        db.session.delete(word_obj)
        db.session.commit()
        return jsonify({'result': 'Deleted'}), 200
    abort(404)
