import os
import requests

from flask import Blueprint, redirect, request, render_template, session, url_for

from configs import spelling_api_address


bp = Blueprint('web', __name__)


def _url(path):
    return spelling_api_address + path


@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/quiz', methods=['POST'])
def quiz():
    name = request.form.get('username')
    total = request.form.get('total')

    path = f'/exam?name={name}&total={total}'
    response = requests.get(_url(path))

    exam_data = response.json()
    data = []
    for idx, q in enumerate(exam_data['questions']):
        data.append((idx, q))
    exam_data['questions'] = data
    session['exam_id'] = exam_data['id']
    session['question_count'] = len(exam_data['questions'])

    return render_template('quiz.html', data=exam_data)

@bp.route('/result', methods=['POST'])
def result():
    answers = []
    for idx in range(session.pop('question_count')):
        answers.append(request.form.get(str(idx)))
    
    data = {'answers': answers}
    exam_id = str(session.pop('exam_id'))
    response = requests.put(_url('/exam/' + exam_id), json=data)

    if response.status_code == 200:
        return render_template('result.html', data=response.json())

    return f"<h1>Something went wrong!</h1><br><p>{response.status_code}</p>"


@bp.route('/words', methods=['GET', 'POST'])
def list_words():
    if request.method == 'POST':
        value = request.form.get('value')
        requests.post(_url('/words'), json={'word': value})

    response = requests.get(_url('/words'))
    return render_template('words.html', data=response.json())

@bp.route('/words/add')
def add_word():
    return render_template('add.html')

@bp.route('/word/<int:word_id>/delete')
def delete_word(word_id):
    requests.delete(_url('/words/' + str(word_id)))
    return redirect(url_for('.list_words'))
