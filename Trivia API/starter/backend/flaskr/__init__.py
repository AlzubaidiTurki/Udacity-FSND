import os
from flask import Flask, request, abort, jsonify
from flask.helpers import url_for
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import sys
from sqlalchemy.sql.expression import false

from werkzeug.utils import redirect

from models import setup_db, Question, Category, db

# $env:FLASK_APP="flaskr"
# $env:FLASK_ENV = "development"

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app,  resources={r"/api/*": {"origins": "*"}})
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


  @app.route('/')
  def index():
    return redirect(url_for('get_all_questions'))
   

  @app.route('/api/categories', methods = ['GET'])
  def get_categories():
    return jsonify({
      'success': True,
      'categories': {category.id: category.type for category in Category.query.all()} #list of categories
    })


  @app.route('/api/questions', methods = ['GET'])
  def get_all_questions():

    page = request.args.get('page', 1 , type=int)
    questions = Question.query.paginate(page, per_page =10)

    return jsonify({
      'success' : True,
      'questions': [question.format() for question in questions.items],
      'totalQuestions': questions.total,
      'categories': {category.id: category.type for category in Category.query.all()},
      'currentCategory': None
    })
 
  @app.route('/api/questions/<int:question_id>', methods = ['DELETE'])
  def delete_questions(question_id):
    try:
      question = Question.query.get(question_id)
      question.delete()
    except:
      db.session.rollback()
      print(f'DELETE error \n {sys.exc_info()}')
      abort(422)

    return jsonify({'success' : True})

  @app.route('/api/questions', methods = ['POST'])
  def add_question():

    body = request.get_json()

    if body is None:
      abort(400)

    if 'searchTerm' in body:
      searchTerm = body['searchTerm']
      print(f'Search term is not none, it is {searchTerm}')
      
      if searchTerm == "":
        questions = Question.query.all()
      else:
        questions = Question.query.filter(Question.question.ilike('%{}%'.format(searchTerm))).all()

      return jsonify({
        'success': True,
        'questions': [question.format() for question in questions],
        'totalQuestions': len(questions),
        'currentCategory': None
        })

    else:
      question = Question(question = body['question'], answer = body['answer'], category=body['category'], difficulty = body['difficulty'])
    try:
      question.insert()
    except:
      db.session.rollback()
      print(f'ADD QUESTION ERORR {sys.exc_info()}')
      abort(500)

    return jsonify({
      'success': True
    })


  @app.route('/api/categories/<int:category_id>/questions', methods = ['GET'])
  def get_questions_by_category(category_id):
    category = Category.query.get(category_id)
    if category is None: #category does not exist
      abort(404)
    else:
      questions = Question.query.filter_by(category = category_id).all() #if that category has no questions, will send empty list.

    return jsonify({
      'success' : True,
      'questions': [question.format() for question in questions],
      'totalQuestions': len(questions),
      'currentCategory': Category.query.get(category_id).type
    })

  @app.route('/api/quizzes', methods = ['POST'])
  def quizzes():
    body = request.get_json()
    previousQuestions = body.get('previous_questions')
    quizCategory = body.get('quiz_category')
    if quizCategory['id'] == 0:
      questions_count = Question.query.count()
    else:
      questions_count = Question.query.filter_by(category = quizCategory['id'] ).count()

    existed_categories = [str(question.category) for question in Question.query.all()]
    
    if len(previousQuestions) == questions_count: # or (quizCategory['id'] not in existed_categories and quizCategory['id'] != 0): # All questions has been shown or there are no questions for that category.
      return jsonify({
        'success': True,
        'question': None
      })

    question = None
    
    while True:
      if question is not None and question.id not in previousQuestions:
        break
      else:
        if quizCategory['id'] == 0:
          question = Question.query.offset(int(Question.query.count() * random.random())).first() #random question.
        else:
          question = Question.query.filter_by(category = quizCategory['id']).offset(int(Question.query.count() * random.random())).first() #random question from a specific category.

    
    return jsonify ({
      'success': True,
      'question': question.format()
    })


  @app.errorhandler(404)
  def not_found(error):
    return jsonify ({
      'success': False,
      'error': 404,
      'message': 'not found'
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False, 
      'error': 422,
      'message': "unprocessable entity"
      }), 422

  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
      'success': False, 
      'error': 500,
      'message': "internal server error"
      }), 500

  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      'success': False,
      'error': 405,
      'message': 'method not allowed'
    }), 405
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'bad request'
    }), 400

  return app

    