## !! SETUP !!
##.venv/scripts/activate

## !! TEST !!
##set FLASK_APP=application.py
##set FLASK_ENV=development
##py -m flask run

from flask import Flask, request
app = Flask(__name__)
from flask_sqlalchemy import SQLAlchemy


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

app.app_context().push()

## !! TERMINAL ADD !!
##py
##from app import app
##from app import db
##db.create_all()
##from app import Book
##book = Book(name="", author="", publisher="")
##db.session.add(book)
##db.session.commit()
##Book.query.all()


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    author = db.Column(db.String(80))
    publisher = db.Column(db.String(80))

    def __repr__(self):
        return f"{self.name} - {self.author} - {self.publisher}"


@app.route('/')
def index():
    return 'Hellooo!'

@app.route('/books')
def get_books():
    books = Book.query.all()
    output = []
    for book in books:
        book_data = {'name': book.name, 'author': book.author, 'publisher': book.publisher}
        output.append(book_data)
    return {"books": output}

@app.route('/books/<id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return {'name': book.name, 'author': book.author, 'publisher': book.publisher}

@app.route('/books', methods=['POST'])
def add_book():
    book = Book(name=request.json['name'], author=request.json['author'], publisher=request.json['publisher'])
    db.session.add(book)
    db.session.commit()
    return {'id': book.id}

@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.get(id)
    if book is None:
        return {"error": "not found"}
    db.session.delete(book)
    db.session.commit()
    return {"message": "dub"}