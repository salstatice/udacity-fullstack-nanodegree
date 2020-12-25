# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior. 

1. Use Flask-CORS to enable cross-domain requests and set response headers. 
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. 
3. Create an endpoint to handle GET requests for all available categories. 
4. Create an endpoint to DELETE question using a question ID. 
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. 
6. Create a POST endpoint to get questions based on category. 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. 
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 
9. Create error handlers for all expected errors including 400, 404, 422 and 500. 

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```

## API Referrence

### Getting Started

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.

- Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:
```
{
    'success': False, 
    'error': 400,
    'message': "Bad request"
}
```

The API will return four error types when requests fail:

- 400: Bad request
- 404: Resource not found
- 405: Methods not found
- 422: Unprocessable

### Endpoints

The API has six endpoints with seven functions:

1. GET '/questions'
2. GET '/categories'
3. GET '/categories/\<int:category_id\>/questions'
4. DELETE '/questions/\<int:question_id\>'
5. POST '/question' *(has two behaviors)*
6. POST '/quizzes'

#### GET '/questions'

##### General

- Fetches a success value, a list of question objects, total number of questions, a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category, and a current_catgegory variable that is unused. `current_category` simply returns the request argument if it exists.

- Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.

**Request Arguments:** None

**Returns:** An object with the following key: 'success', 'questions', 'total_questions', 'categories', 'current_category' 
```
{
  'success': True,
  'questions': [{
                  'id': 1,
                  'question': "What is the question?",
                  'answer': "This is the answer",
                  'category': "3",
                  'difficulty': 5
                },{
                  'id': 2,
                  'question': "What is question #2?",
                  'answer': "This is answer #2",
                  'category': "1",
                  'difficulty': 4
                }],
  'total_questions': 2,
  'categories': {'1' : "Science",
                  '2' : "Art",
                  '3' : "Geography",
                  '4' : "History",
                  '5' : "Entertainment",
                  '6' : "Sports"},
  'current_category': ""
}
```

#### GET '/categories'

##### General

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category

**Request Arguments:** None

**Returns:** An object with a single key, categories, that contains a object of id: category_string key:value pairs, and a success value
```
{
  'success': True,
  'categories': {'1' : "Science",
                 '2' : "Art",
                 '3' : "Geography",
                 '4' : "History",
                 '5' : "Entertainment",
                 '6' : "Sports"}
}
```

#### GET '/categories/\<int:category_id\>/questions'

##### General

- Fetches an unorder list of questions from a category. Return a empty list if there is no question in the requested category.

**Request Arguments:** <int:cagtegory_id>

**Returns:** An object with the following keys: questions, that contains a list of question objects; total_questions, that contains the number of questions found; current_category, that contains the id of the reqested category; and a success value.
```
{
  'success': True,
  'questions': [{
                  'id': 1,
                  'question': "What is the question?",
                  'answer': "This is the answer",
                  'category': "3",
                  'difficulty': 5
                },{
                  'id': 2,
                  'question': "What is question #2?",
                  'answer': "This is answer #2",
                  'category': "1",
                  'difficulty': 4
                }],
  'total_questions': 2,
  'current_category': 1
}
```

#### DELETE '/questions/\<int:question_id\>'

##### General

- Deletes a question by the question id from the database. Return 404 error if the question is not in the database.

**Request Arguments:** <int:question_id>

**Returns:** An object with a single key, deleted, that contains the id of the question that has been deleted, and a success value.
```
{
  'success': True,
  'deleted': 1
}
```

#### POST '/questions'

##### General

- This endpoint has two behaviors, depends on the variable in the request body JSON object.
 1. Searches and fetech questions that contain substring of the search term.
 2. Inserts a questions to the database
 
- The endpoint prioritize search behavior over insert if the request body contains a object of 'searchTerm': search_term_string key:value pairs.

**Request Arguments:** JSON objects in the following format:
```
{'searchTerm': "searching"}
```
or
```
{
  'question': 'What is the new Question?',
  'answer': 'This is the new Answer',
  'difficulty': 5,
  'category': 2,
}
```

**Returns:** 

`Search`: An object with the following keys: questions, that contains a list of question object in which the substring of the question matches the search term; total_questions, that contains the number of questions that match the search; and a success value.
```
{
  'success': True,
  'questions': [{
                  'id': 1,
                  'question': "What is the question?",
                  'answer': "This is the answer",
                  'category': "3",
                  'difficulty': 5
                },{
                  'id': 2,
                  'question': "What is question #2?",
                  'answer': "This is answer #2",
                  'category': "1",
                  'difficulty': 4
                }],
  'total_questions': 2
}
```
`Insert`: An object with a single key, question_id, that contains the id of the question that has been inserted, and a success value.
```
{
  'success': True,
  'question_id': 12
}
```

#### POST '/quizzes'

##### General

- Fetches a question object in which has the following keys: 'id', 'question', 'answer', 'category' and 'difficulty'.

- The question can be chosen from one particular catergory using the category id and type, or chosen from all category using {'id':0}. The previous questions are excluded from the selection pool. Quiz category and previous questions are default to `id:0` and empty `[]` if the arguments are not provided.

**Request Arguments:** JSON objects in the following format:
```
{
  'previous_questions': [10, 15, 20],
  'quiz_category': {'type': None, 'id': 0}
}
```

**Returns:** An object with a single key, questions, that contains a single question object, and a success value
```
{
  'success': True,
  'questions': {'id': 1,
                'question': "What is the question?",
                'answer': "This is the answer",
                'category': "3",
                'difficulty': 5}
}
```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
