from flask import Flask, render_template, redirect,  url_for, request
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
import sys

from werkzeug.utils import redirect

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(), nullable= False)
    author = db.Column(db.String(), nullable= False)
    type = db.Column(db.String())
    read = db.Column(db.Boolean, default = False)



# inserting records, books i read (and recommend!) and books i would like to read :)
try:
    book1 = Book(title = 'Man\'s Search for Meaning', author = 'Viktor E. Frankl', type = 'Psychology', read = True)
    book2 = Book(title = 'Digital Minimalism: Choosing a Focused Life in a Noisy World ', author = 'Cal Newport', type = 'productivity/life style', read = True )
    book3 = Book (title = 'The Picture of Dorian Gray', author = 'Oscar Wilde', type = 'Novel', read= False)
    books = [book1, book2, book3]
    db.session.add_all(books)
    db.session.commit()
except:
    print(sys.exc_info())
    db.session.rollback()

db.create_all()
@app.route('/')
def index():
    return render_template('my-books.html', books = Book.query.all())

@app.route('/add-book', methods= ['POST', 'GET'])
def addBook():
    try:
        title = request.get_json()['title']
        author = request.get_json()['author']
        type =  request.get_json()['type']

        book = Book(title = title, author = author, type = type, read = False)
        db.session.add(book)
        db.session.commit()
    except:
        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()
        return render_template('add-book.html')

@app.route('/<bookId>/book-read',  methods = ['PUT'])
def book_read(bookId):
    try:
        book = Book.query.get(bookId)
        book.read = True
        db.session.commit()
    except:
        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()
        return redirect(url_for('my-books'))

@app.route('/<bookId>/book-delete',  methods = ['DELETE'])
def book_delete(bookId):
    try:
        book = Book.query.get(bookId)
        db.session.delete(book)
        db.session.commit()
    except:
        print(sys.exc_info())
        db.session.rollback()
    finally:
        db.session.close()
        return redirect(url_for('my-books'))


# Default port:
if __name__ == '__main__':
    app.run(debug=True)