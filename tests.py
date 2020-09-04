import requests
import unittest

from configs import ApiConfig
from models import db
from utils import check_answers
from spelling_api import create_app


class TestConfig(ApiConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class TestWordManagement(unittest.TestCase):
    # Testing response codes only

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all(app=self.app)

        self.tester = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_words(self):
        response = self.tester.get('/words')
        self.assertEqual(response.status_code, 200)

    def test_add_word(self):
        response = self.tester.post('/words', json=dict(word='bagoly'))
        self.assertEqual(response.status_code, 201)

    def test_add_invalid_word(self):
        response = self.tester.post('/words', json=dict(word='valami'))
        self.assertEqual(response.status_code, 400)

    def test_add_duplicate_word(self):
        response = self.tester.post('/words', json=dict(word='bagoly'))
        self.assertEqual(response.status_code, 201)

        response = self.tester.post('/words', json=dict(word='bagoly'))
        self.assertEqual(response.status_code, 409)

    def test_delete_word(self):
        response = self.tester.post('/words', json=dict(word='bagoly'))
        self.assertEqual(response.status_code, 201)

        word_id = response.json['word_id']
        response = self.tester.delete('/words/' + str(word_id))
        self.assertEqual(response.status_code, 200)

    def test_delete_non_existent_word(self):
        response = self.tester.delete('/words/' + str(99))
        self.assertEqual(response.status_code, 404)


class TestCheckAnswer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.words = ['bagoly', 'vajas']

    def test_is_correct_valid_success(self):
        # Right spelling, user answer successfully
        original = ['bagoly', 'vajas']
        answers = ['y', 'y']

        value = check_answers(original, answers, self.words)
        self.assertEqual(2, sum(value))

    def test_is_correct_valid_failed(self):
        # Right spelling, user answer unsuccessfully
        original = ['bagoly', 'vajas']
        answers = ['n', 'n']

        value = check_answers(original, answers, self.words)
        self.assertEqual(0, sum(value))

    def test_is_correct_invalid_success(self):
        # Wrong spelling, user answer successfully
        original = ['bagoj', 'valyas']
        answers = ['n', 'n']

        value = check_answers(original, answers, self.words)
        self.assertEqual(2, sum(value))

    def test_is_correct_invalid_failed(self):
        # Wrong spelling, user answer unsuccessfully
        original = ['bagoj', 'valyas']
        answers = ['y', 'y']

        value = check_answers(original, answers, self.words)
        self.assertEqual(0, sum(value))

    def test_fill_empty_success(self):
        # User answer successfully
        original = ['bago_', 'va_as']
        answers = ['ly', 'j']

        value = check_answers(original, answers, self.words)
        self.assertEqual(2, sum(value))

    def test_fill_empty_failed(self):
        # User answer unsuccessfully
        original = ['bago_', 'va_as']
        answers = ['j', 'ly']

        value = check_answers(original, answers, self.words)
        self.assertEqual(0, sum(value))


if __name__ == "__main__":
    unittest.main(verbosity=2)
