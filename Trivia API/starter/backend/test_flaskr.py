import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import math
from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')  
        self.DB_USER = os.getenv('DB_USER', 'postgres')  
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')  
        self.DB_NAME = os.getenv('DB_NAME', 'trivia')  
        self.DB_PATH = 'postgresql+psycopg2://{}:{}@{}/{}'.format(self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_NAME)
        setup_db(self.app, self.DB_PATH)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_valid_paginated(self):
        res = self.client().get('/api/questions')
        data = json.loads(res.data)
        categories = {category.id: category.type for category in Category.query.all()}
        self.assertEqual(data['categories'], categories) #something weird happens in this test it shows:
                                                        #AssertionError: {'1': 'Science', '2': 'Art', '3': 'Geograp[52 chars]rts'} != {1: 'Science', 2: 'Art', 3: 'Geography', 4[40 chars]rts'}
        self.assertTrue(data['success'])
        self.assertGreater(data['totalQuestions'], 1)
        self.assertEqual(res.status_code, 200)
    


    def test_invalid_paginated(self):
        total_questions = Question.query.count()
        per_page = 10 #ten questions per page
        pages = math.ceil(total_questions/per_page)
        res = self.client().get(f'/api/questions?page={pages+1}') #pages+1 always not found.
        data= json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'not found')
        self.assertEqual(data['error'], 404)

    def test_valid_delete(self):
        question = Question.query.first()
        res = self.client().delete(f'/api/questions/{question.id}')
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200) 

    def test_invalid_delete(self):
        question_id = 0 #a question that does not exists.
        res = self.client().delete(f'/api/questions/{question_id}')
        data= json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable entity')
        self.assertEqual(data['error'], 422)

    def test_search(self): #no failure scinario in this use case, empty list is still successful search.
        search_term = ''
        res = self.client().post('/api/questions', json = {'searchTerm': search_term})
        data = json.loads(res.data)
        if search_term == '':
            questions = Question.query.all()
        else:
            questions = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).all()
        
        questions_formatted = [question.format() for question in questions]
        self.assertTrue(data['success'])
        self.assertEquals(data['questions'], questions_formatted)
        self.assertEquals(data['totalQuestions'], len(questions))
        self.assertEqual(res.status_code, 200)

    def test_valid_sumbit_question(self):
        question = {'question' : 'what is the BEST sitcom show?', 'answer': 'the office', 'category': 2, 'difficulty' : 5}
        res = self.client().post('/api/questions', json = question)
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(res.status_code, 200)

    def test_invalid_sumbit_question(self):
        false_question = {'question' : 'what is the BEST sitcom show?', 'category': 2, 'difficulty' : 5} #no answer given
        res = self.client().post('/api/questions', json = false_question)
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'internal server error')
        self.assertEqual(data['error'], 500)
        self.assertEqual(res.status_code, 500)

    def test_valid_get_by_category(self):
        category = Category.query.first()
        res = self.client().get(f'/api/categories/{category.id}/questions')
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertGreater(data['totalQuestions'], 0)
        self.assertEqual(data['currentCategory'], category.type)
        self.assertEqual(res.status_code, 200)
        
    def test_invalid_get_by_category(self):
        category_id = 10 #category does not exist.
        res = self.client().get(f'/api/categories/{category_id}/questions')
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'not found')
        self.assertEqual(data['error'], 404)
        self.assertEqual(res.status_code, 404)
        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()