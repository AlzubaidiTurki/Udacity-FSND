from functools import reduce
import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink, db
from .auth.auth import AuthError, requires_auth
import sys

# $ENV:FLASK_APP="api.py"
# $ENV:FLASK_ENV='development'

app = Flask(__name__)
setup_db(app)
CORS(app)


#db_drop_and_create_all()

# ROUTES
@app.route('/drinks', methods = ['GET'])
def get_drinks():
    
    try:
        drinks = Drink.query.all()  

    except:
        print(f'yata_get_drinks ERROR {sys.exc_info()}')
        abort(500)
    
    drinks_short = [drink.short() for drink in drinks]
    
    return jsonify({
        'success': True,
        'drinks': drinks_short
    })
    

@app.route('/drinks-detail', methods = ['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(_):
    try:
        drinks = Drink.query.all()
    except:
        print(f'yata_get_drinks_detail ERROR {sys.exc_info()}')
        abort(500) #Internal server error

    drinks_long = [drink.long() for drink in drinks]

    return jsonify({
        'success': True,
        'drinks': drinks_long
    })


@app.route('/drinks', methods = ['POST'])
@requires_auth('post:drinks')
def post_drink(_):
    data = request.get_json()
    title = data['title']
    recipe = json.dumps(data['recipe'])

    try:
        drink = Drink (title= title, recipe = recipe)
        drink.insert()
    except:
        print(f'yata_post_drink ERROR {sys.exc_info()}')
        db.session.rollback()
        abort(500)
    
    return jsonify({
        'success': True,
        'drinks': [drink.long()]
    })


@app.route('/drinks/<int:drink_id>', methods = ['PATCH'])
@requires_auth('patch:drinks')
def patch_drink(_, drink_id):

    drink = Drink.query.get(drink_id)

    if drink is None:
        abort(404)

    data = request.get_json()
    title = data['title']
    flag = False
    if 'recipe' in data:
        flag = True
        recipe = json.dumps(data['recipe'])

    try:
        drink.title = title
        if flag:
            drink.recipe = recipe
    except:
        print(f'yata_patch_drink ERROR {sys.exc_info()}')
        db.session.rollback()
        abort(500)

    return jsonify({
        'success': True,
        'drinks': [drink.long()]
    })


@app.route('/drinks/<int:drink_id>', methods = ['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(_, drink_id):
    drink = Drink.query.get(drink_id)

    if drink is None:
        abort(404)
    
    try:
        drink.delete()
    except:
        db.session.rollback()
        print(f'yata_delete_drink ERROR {sys.exc_info()}')
        abort(500)
    
    return jsonify({
        'success': True,
        'delete': drink.id
    })

# Error Handling
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

@app.errorhandler(500)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal Server Error"
    }), 500

@app.errorhandler(AuthError)
def auth_errors(auth_error):
    return jsonify({
        'success': False,
        'error': auth_error.status_code,
        'message': auth_error.error
    }), auth_error.status_code