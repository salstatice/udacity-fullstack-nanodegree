import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

## ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['GET'])
def get_short_drink_recipe():
    try:
        drinks = Drink.query.all()
        
        formatted_drinks = [drink.short() for drink in drinks]
        
        return jsonify({
            'success': True,
            'drinks': formatted_drinks
        })
    except:
        abort(422)

'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_long_drink_recipe(payload):
    try:
        drinks = Drink.query.all()
        formatted_drinks = [drink.long() for drink in drinks]
        return jsonify({
            'success': True,
            'drinks': formatted_drinks
        })
    except:
        abort(422)

'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_new_drink(payload):
    body = request.get_json()
    if body is None:
      abort(400)
    
    req_title = body.get('title')
    req_recipe = body.get('recipe')
    
    try:
        ## abort 400 bad request if title is duplicated
        if Drink.query.filter(Drink.title==req_title).all():
            abort(400)
        
        drink = Drink(title=req_title, recipe=json.dumps(req_recipe))
        drink.insert()
        
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })
    except Exception as e:
        if e.code == 400:
            abort(400)
        else:
            abort(422)

'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def edit_drink_recipe(payload, id):
    body = request.get_json()
    if body is None:
        abort(400)

    try:
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if not drink:
            abort(404)

        if body.get('title'):
            drink.title = body.get('title')
        elif body.get('recipe'):
            drink.recipe = json.dumps(body.get('recipe'))
        else:
            abort(400)

        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })
    except Exception as e:
        if e.code == 404:
            abort(404)
        else:
            abort(422)

'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    try:
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if not drink:
            abort(404)
        
        drink.delete()

        return jsonify({
            'success': True
        })
    except Exception as e:
        if e.code == 404:
            abort(404)
        else:
            abort(422)

## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

'''
@TODO implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'bad request'
    }), 400

'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''
@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
                "success": False, 
                "error": 404,
                "message": "resource not found"
                }), 404

'''
@TODO implement error handler for AuthError
    error handler should conform to general task above 
'''
@app.errorhandler(AuthError)
def auth_error(e):
    return jsonify(e.error), e.status_code