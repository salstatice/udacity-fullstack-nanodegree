import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from sqlalchemy import func

from models import setup_db, db, Question, Category

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start = (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  formatted_questions = [question.format() for question in selection]
  current_questions = formatted_questions[start:end]

  return current_questions

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
    try:
      questions = Question.query.all()
      questions_count = Question.query.count()
      current_questions = paginate_questions(request, questions)

      if len(current_questions) == 0:
        abort(404)

      current_category = request.args.get('currentCategory', None)
      categories = Category.query.all()
      formatted_categories = {category.id: category.type for category in categories}

      return jsonify({
        'success': True,
        'questions': current_questions,
        'total_questions': questions_count,
        'categories': formatted_categories,
        'current_category': current_category
      })
    except Exception as e:
      if e.code == 404:
        abort(404)
      else:
        abort(422)
    finally:
      db.session.close()

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/categories', methods=['GET'])
  def get_categories_list():
    try:
      categories = Category.query.all()
      formatted_categories = {category.id:category.type for category in categories}

      return jsonify({
        'success': True,
        'categories': formatted_categories
      })
    except:
      abort(422)
    finally:
      db.session.close()

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def get_quesions_by_categories(category_id):
    try:
      # check if category exists
      category = Category.query.filter(Category.id == category_id).one_or_none()
      if category is None:
        abort(404)
      
      questions = Question.query.filter(Question.category == category_id).all()
      questions_count = Question.query.filter(Question.category == category_id).count()
      if questions_count == 0:
        formmatted_questions = []
      else:
        formatted_questions = [question.format() for question in questions]

      return jsonify({
        'success': True,
        'questions': formatted_questions,
        'total_questions': questions_count,
        'current_category': category_id
      })
    except Exception as e:
      if e.code == 404:
        abort(404)
      else:
        abort(422)
    finally:
      db.session.close()

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
  @app.route('/questions', methods=['POST'])
  def create_question():
    '''
    This endpoint handle two functions: 
    1) Add a new questions
    2) If there is a search_term, perform a search instead
    '''
    body = request.get_json()
    if body is None:
      abort(400)

    new_question = body.get('question', None)
    new_answer = body.get('answer', None)
    new_difficuly = body.get('difficulty', None)
    new_category = body.get('category', None)
    search_term = body.get('searchTerm', None)

    try:
      # perform search
      if search_term:
        questions = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).order_by(Question.id).all()
        total_questions = Question.query.filter(Question.question.ilike('%{}%'.format(search_term))).order_by(Question.id).count()
        if total_questions == 0:
          formatted_questions = []
        else:
          formatted_questions = [question.format() for question in questions]
        return jsonify({
          'success': True,
          'questions': formatted_questions,
          'total_questions': total_questions
        })
      # post a new question
      elif new_question and new_answer and new_difficuly:
        question = Question(question=new_question, answer=new_answer, difficulty=new_difficuly, category=new_category)
        question.insert()
        new_id = question.id
        return jsonify({
          'success': True,
          'question_id': new_id
        })
      else:
        abort(400)
    except Exception as e:
      if e.code == 400:
        abort(400)
      else:
        db.session.rollback()
        abort(422)
    finally:
      db.session.close()
  

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
  @app.route('/quizzes', methods=['POST'])
  def get_next_question():
    body = request.get_json()
    if body is None:
      abort(400)

    previous_questions = body.get('previous_questions', [])
    quiz_category = body.get('quiz_category', {'id': 0})

    try:
      # for all catergories
      if quiz_category['id'] == 0 :
        if not previous_questions:
          question = Question.query.order_by(func.random()).first()
        else:
          question = Question.query.filter(Question.id.notin_(previous_questions)).order_by(func.random()).first()
        
        # if database still have more unused questions
        if question:
          return jsonify({
            'success': True,
            'question': question.format()
          })
        else:
          return jsonify({
            'success': True,
            'question': None
          })
      # for one catergory
      else:
        if not previous_questions:
          question = Question.query.filter(Question.category == quiz_category['id']).order_by(func.random()).first()
        else:
          question = Question.query.filter(Question.category == quiz_category['id']).filter(Question.id.notin_(previous_questions)).order_by(func.random()).first()
        
        # if database still have more unused questions
        if question:
          return jsonify({
            'success': True,
            'question': question.format()
          })
        else:
          return jsonify({
            'success': True,
            'question': None
          })
    except:
      abort(422)
    finally:
      db.session.close()


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

  @app.errorhandler(405)
  def methods_not_found(error):
    return jsonify({
      'success': False,
      'error': 405,
      'message': 'Methods not found'
    }), 405

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'Unprocessable'
    }), 422

  return app

    