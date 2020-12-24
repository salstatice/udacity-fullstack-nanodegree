import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)
  # Another way to do it:
  # cors = CORS(app, RESOURCES={r"*/api/*": {"origins":'*'}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authroization')
    response.headers.add('Access-Copntrol-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response
  
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_all_categories():
    categories = Category.query.all()
    formatted_categories = [category.format() for category in categories]

    return jsonify({
      'success': True,
      'categories': formatted_categories
    })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  def get_paginated_questions():
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = Question.query.all()
    questions_count = Question.query.count()
    formatted_questions = [question.format() for question in questions]

    current_category = request.args.get('currentCategory', None)
    categories = Category.query.all()
    formatted_categories = [category.format() for category in categories]

    return jsonify({
      'success': True,
      'questions': formatted_questions[start:end],
      'total_questions': questions_count,
      'categories': formatted_categories,
      'current_category': current_category
    })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_questions(question_id):
    try:
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404)
      question.delete()
      return jsonify({
        'success': True,
        'deleted': question_id,
      })
    except Exception as e:
      if e.code == 404:
        abort(404)
      else:
        db.session.rollback()
        abort(422)
    finally:
      db.session.close()

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  # waiting on clarification from mentors
  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/questions', methods=['POST'])
  def create_question():
    body = request.get_json()

    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_difficuly = body.get('difficulty', None)
    new_category = body.get('category', None)
    search_term = body.get('searchTerm', None)
    get_by_category = body.get('getGatergory', None)

    try:
      if search_term:
        return jsonsify({
          'search': 'something'
        })
      elif get_by_category:
        return jsonsify({
          'question': []
        })
      else:
        question = Question(question=new_question, answer=new_answer, difficulty=new_difficuly, category=new_category)
        question.insert()
        new_id = question.id
        return jsonify({
          'success': True,
          'question_id': new_id
        })
    except:
      abort(422)

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      'success': False,
      'error': 400,
      'message': 'Bad request'
    }), 400

  @app.errorhandler(404)
  def resource_not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'Resource not found'
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'Unprocessable'
    }), 422

  return app

    