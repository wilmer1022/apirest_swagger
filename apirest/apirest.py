#!flask/bin/python

from flask import Flask, jsonify, send_from_directory
from flask import abort
from flask import request
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from marshmallow import Schema, fields
from datetime import date
from flask import render_template

app = Flask(__name__, instance_relative_config=True)

books = [
    {
        'id': 1,
        'title': 'La hojarasca',
        'description': 'Good one',
        'author': 'Gabo'
    },
    {
        'id': 2,
        'title': 'El coronel no tiene quien le escriba',
        'description': 'Interesting',
        'author': 'Gabo'
    }
]

spec = APISpec(
    title='Flask-api-swagger-doc',
    version='1.0.0.',
    openapi_version='3.0.2',
    plugins=[FlaskPlugin(),MarshmallowPlugin()]
)

@app.route('/api/swagger.json')
def create_swagger_spec():
        return jsonify(spec.to_dict())

class BookResponseSchema(Schema):
        id = fields.Int()
        title = fields.Str()
        description = fields.Str()
        author = fields.Str()

class DeleteResponseSchema(Schema):
        result = fields.Bool()

class BookListResponseSchema(Schema):
        book_list = fields.List(fields.Nested(BookResponseSchema))

# Get all books
# For testing: curl -i http://localhost:5000/books
@app.route('/books', methods=['GET'])
def get_books():
    """Get List of Books
        ---
        get:
            description: Get List of Books
            responses:
                200:
                    description: Return an book list
                    content:
                        application/json:
                            schema: BookListResponseSchema
    """
    return BookListResponseSchema().dump({'book_list':books})

# Get one book by id
# For testing: curl -i http://localhost:5000/books/2
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Get Book by ID
        ---
        get:
            description: Get Book by ID
            responses:
                200:
                    description: Return an book
                    content:
                        application/json:
                            schema: BookResponseSchema
    """
    book = [book for book in books if book['id'] == book_id]
    if len(book) == 0:
        abort(404)
    return BookResponseSchema().dump(book[0])

# Add new book
# For testing: curl -i -H "Content-Type: application/json" -X POST -d '{"title":"El libro"}' http://localhost:5000/books
@app.route('/books', methods=['POST'])
def create_book():
    """Post create a Book
        ---
        post:
            description: Post create a book
            responses:
                200:
                    description: Create an book
                    content:
                        application/json:
                            schema: BookListResponseSchema
    """
    if not request.json or not 'title' in request.json:
        abort(400)
    book = {
        'id': books[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'author': request.json.get('author', ""),
    }
    books.append(book)
    return BookListResponseSchema().dump({'book_list':books}), 201

# Edit a Book
# For testing: curl -i -H "Content-Type: application/json" -X PUT -d '{"author":"Jorgito"}' http://localhost:5000/books/2
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """Put update a Book
        ---
        put:
            description: Put update a book
            responses:
                200:
                    description: Update an book
                    content:
                        application/json:
                            schema: BookResponseSchema
    """
    book = [book for book in books if book['id'] == book_id]
    if len(book) == 0 or not request.json:
        abort(404)
    book[0]['title'] = request.json.get('title', book[0]['title'])
    book[0]['description'] = request.json.get('description', book[0]['description'])
    book[0]['author'] = request.json.get('author', book[0]['author'])
    return BookResponseSchema().dump(book[0])
    
# Delete a Book
# For testing: curl -i -H "Content-Type: application/json" -X DELETE http://localhost:5000/books/1
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """Delete a Book
        ---
        delete:
            description: Delete a book
            responses:
                200:
                    description: Delete an book
                    content:
                        application/json:
                            schema: DeleteResponseSchema
    """
    book = [book for book in books if book['id'] == book_id]
    if len(book) == 0:
        abort(404)
    books.remove(book[0])
    return DeleteResponseSchema().dump({'result': True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

with app.test_request_context():
    spec.path(view=get_books)
    spec.path(view=get_book)
    spec.path(view=create_book)
    spec.path(view=update_book)
    spec.path(view=delete_book)

@app.route('/docs')
@app.route('/docs/<path:path>')
def swagger_docs(path=None):
    if not path or path == 'index.html':
        return render_template('index.html',base_url='/docs')
    else:
        return send_from_directory('static',path)
        
 if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)