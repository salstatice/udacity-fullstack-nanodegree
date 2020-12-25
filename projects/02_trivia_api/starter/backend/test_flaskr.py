import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.databause_user = ""
        self.database_path = "postgres://{}@{}/{}".format(self.databause_user, 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # new question use for testing
        self.new_question = {
            'question': 'What is the Question?',
            'answer': 'This is the Answer',
            'difficulty': 5,
            'category': 2,
        }
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # Test get paginated questions

    def test_get_paginated_questions_without_args(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))
        self.assertEqual(data['current_category'], None)

    def test_get_paginated_questions_with_args(self):
        res = self.client().get('/questions?page=2&currentCategory=3')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['categories']))
        self.assertTrue(data['current_category'])

    def test_404_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=100000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource not found')

    # Test get list of categories

    def test_get_categories_list(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))
        self.assertEqual(data['categories']['2'],'Art')

    def test_get_categories_list_with_bad_endpoint(self):
        res = self.client().get('/categories/asdfasdf')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource not found')
    
    def test_get_categories_list_with_invalid_methods(self):
        res = self.client().post('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 405)
        self.assertEqual(data['message'], 'Methods not found')

    # Test get questions by categories

    def test_get_questions_by_categories(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertEqual(data['total_questions'], 3)
        self.assertEqual(data['current_category'], 1)

    def test_404_get_questions_by_invalid_categories(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'Resource not found')


    # Test delete question

    def test_delete_existing_question(self):
        # add a new question to use for deletion
        add_res = self.client().post('/questions', json=self.new_question)
        add_data = json.loads(add_res.data)
        # test deletion
        ques_id = str(add_data['question_id'])
        res = self.client().delete('/questions/'+ ques_id )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], add_data['question_id'])

    def test_404_for_delele_non_existing_question(self):
        res = self.client().delete('/questions/10000' )
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # Test add new question  

    def test_add_new_question(self):
        # Test adding a new question
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        # delete question after a successful add request to keep database consistancy
        ques_id = str(data['question_id'])
        del_res = self.client().delete('/questions/'+ ques_id )
        del_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question_id'])

    def test_400_add_new_question_with_no_request_body(self):
        res = self.client().post('/questions')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Bad request')

    def test_400_add_new_question_with_bad_param(self):
        res = self.client().post('/questions', json={'question': None,})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Bad request')

    # Test search questions

    def test_search_questions_with_result(self):
        res = self.client().post('/questions', json={'searchTerm': 'paint'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertEqual(data['total_questions'], 2)

    def test_search_questions_without_result(self):
        res = self.client().post('/questions', json={'searchTerm': 'bubbletea'})
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], 0)    


    # tests for POST '/quizzes'
    
    def test_play_quizzes_first_question_all_categories(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': None,
            'quiz_category': {'type': None, 'id': 0}
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_play_quizzes_next_question_all_categories(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': [10, 15, 20],
            'quiz_category': {'type': None, 'id': 0}
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
    
    def test_play_quizzes_with_no_more_question_all_categories(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': [5,9,2,4,6,10,11,12,13,14,15,16,17,18,19,20,21,22,23],
            'quiz_category': {'type': None, 'id': 0}
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertFalse(data['question'])

    def test_play_quizzes_first_question_one_categories(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': [],
            'quiz_category': {'type': 'Art','id': 2}
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_play_quizzes_next_question_one_categories(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': [16, 17],
            'quiz_category': {'type': 'Art', 'id': 2}
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
    
    def test_play_quizzes_with_no_more_question_one_categories(self):
        res = self.client().post('/quizzes', json={
            'previous_questions': [16, 17, 18, 19],
            'quiz_category': {'type': 'Art', 'id': 2}
            })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertFalse(data['question'])
    
    def test_400_play_quizzes_with_no_request_body(self):
        res = self.client().post('/quizzes')
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], 'Bad request')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()