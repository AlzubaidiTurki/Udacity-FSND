import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Course
from collections import OrderedDict
import dateutil.parser


class UniversityTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = "postgresql://postgres: @localhost:5432/api_test"
        setup_db(self.app, self.database_path)

        self.new_course = {
            'name': 'man\'s search for meaning',
            'semester': 3,
        }
        self.false_new_Course = {
            'name' : 'Calculs'
        }

        self.new_student = {
            'name': 'Test Student',
            'email': 'student@student.com',
        }

        self.new_professor = {
            'name': 'Test Professor',
            'email': 'professor@professor.com',
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        self.courses_count = Course.query.count()
        self.formmated_courses = [course.format() for course in Course.query.all()]

    # in json, created_at key always on top, this function makes everything propoer
    def getOrderedDict(data):
        
        created_at = data['course']['created_at']
        ordered_dict = OrderedDict()
        ordered_dict['created_at'] = created_at
        del data['course']['created_at']

        for key, value in data.items():
            ordered_dict[key] = value

        return ordered_dict
        

    def tearDown(self):
        """Executed after reach test"""
        pass

    
    def test_get_all(self):
        """Test _____________ """
        res = self.client().get('/courses')
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['courses'], self.formmated_courses)
        self.assertEqual(data['total_courses'], self.courses_count)
        self.assertEqual(res.status_code, 200)
        
    def test_invalid_page_number(self):
        res = self.client().get('/courses?page=10')
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'unprocessable')
        self.assertEqual(res.status_code, 422)

    def test_valid_get_a_course(self):
        res = self.client().get('/courses/11')
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        course = Course.query.get(11).format()
        self.assertEqual(data['course'], course)
        self.assertEqual(res.status_code, 200)

    def test_invalid_get_a_course(self):
        res = self.client().get('/courses/1000')
        data = json.loads(res.data)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')
        self.assertEqual(res.status_code, 404)
    

    def test_success_post(self):
        res = self.client().post('/courses', json=self.new_course)

        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['course'], Course.query.filter_by(name = self.new_course['name']).first().format())

    def test_unsuccess_post(self):
        res = self.client().post('/courses', json=self.false_new_Course)
        self.assertEqual(res.status_code, 500)
    
    def test_success_delete(self):
        course = Course.query.get(9)
        res = self.client().delete('/courses/9')
        data = json.loads(res.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['course'], course.id)
    
    def test_unsuccess_delete(self):
        res = self.client().delete('/courses/3')
        data = json.loads(res.data)
        self.assertEqual(data['message'], 'resource not found')
        self.assertEqual(res.status_code, 404)
    



if __name__ == "__main__":
    unittest.main()
