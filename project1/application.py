#=============================PROJECT 1========================================
#==========================WEB PROGRAMMING========================
#=========================NAME: JONNATHAN FABRICIO CRESPO YAGUANA=============
#==========================DATE: DECEMBER 2019=================================

#=========IMPORT STATEMENTS======================

import os
from flask import Flask, session, render_template, request, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
from functools import wraps #Para login_required

#==============DEFINE A DECORATOR===================

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("username") is None:
            return redirect("/signin")
        return f(*args, **kwargs)
    return decorated_function

#=========================================================


app = Flask(__name__)

# Check for environment variable
#if not os.getenv("postgres://kjkmtwcexbgcrx:522c649866896ff5bddbbbb0c53f2dec216fb496e6590bdce81f42e5aba9f313@ec2-174-129-253-47.compute-1.amazonaws.com:5432/d98hjgkripkjc5"):
#    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"


Session(app)

# Set up database
engine = create_engine("postgres://kjkmtwcexbgcrx:522c649866896ff5bddbbbb0c53f2dec216fb496e6590bdce81f42e5aba9f313@ec2-174-129-253-47.compute-1.amazonaws.com:5432/d98hjgkripkjc5")
db = scoped_session(sessionmaker(bind=engine))

#=====================DEFINE ROUTES============================
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def login():

    #Get form information
    username = request.form.get("username") #variable recibida del campo username de indeX.html
    password= request.form.get("password")
    #Session close
    session.pop('user', None)

    # Make sure user exist.
    if db.execute("SELECT * FROM users WHERE (username = :username) and (password = :password)", {"username":username, "password":password}).rowcount==0:
        return render_template("error.html", message="Username or password invalid")
    #Make sure acount_state is inactive
    if db.execute("SELECT * FROM users WHERE (username = :username) and (password = :password) and (count_state='True')", {"username":username, "password":password}).rowcount==1:
        return render_template("error.html", message="You have already login in your account")
    #ACTIVE SESSION
    session['user']=username
    #If user login, count_state=True
    db.execute("UPDATE users SET count_state=True  WHERE (username = :username) and (password = :password)", {"username":username, "password":password})
    db.commit()
    return render_template("personal_account.html")

@app.route("/signup", methods=["POST"])
def signup():

    #Get information
    username1 = request.form.get("username1") #variable recibida del campo username de indeX.html
    password1= request.form.get("password1")
    name = request.form.get("name") #variable recibida del campo username de indeX.html
    lastname= request.form.get("lastname")

    db.execute("INSERT INTO users (username, password, name, last_name) VALUES (:username, :password, :name, :lastname)",
            {"username": username1, "password":password1, "name":name, "lastname": lastname})
    db.commit()
    return render_template("success.html")

@app.route("/logout", methods=["POST"])
def logout():
    #Get username
    user1=session['user']
    #Update user_account
    db.execute("UPDATE users SET count_state=False  WHERE (username = :username)", {"username":user1})
    db.commit()
    #close session
    session.pop('user', None)
    return render_template("index.html")

#Search by isbn
@app.route("/books_isbn", methods=["POST", "GET"])
@login_required
def books_isbn():
    """List all books."""
    isbn=request.form.get("isbn")
    isbn=isbn+'%'
    if db.execute("SELECT * FROM books WHERE (isbn similar to :isbn)", {"isbn":isbn}).rowcount==0:
        return render_template("error.html", message= "No matches with the ISBN specified")
    books=db.execute("SELECT * FROM books WHERE (isbn similar to :isbn)", {"isbn": isbn})
    db.commit()
    return render_template("isbn.html", books=books)

#Specific book
@app.route("/books_isbn/<string:book_isbn>")
@login_required
def bookisbn(book_isbn):
    """List details about a single book."""

    # Make sure flight exists.
    books=db.execute("SELECT * FROM books WHERE (isbn=:book_isbn)", {"book_isbn": book_isbn})
    reviews=db.execute("SELECT * FROM reviews WHERE (isbn_review=:book_isbn)", {"book_isbn": book_isbn})
    reviews_avg= db.execute ("SELECT round(avg(review::integer),1) as average, count(*) as count from reviews where (isbn_review =:book_isbn)", {"book_isbn": book_isbn})
    db.commit()
    return render_template("book.html", books=books, reviews=reviews, reviews_avg=reviews_avg)

#search by title
@app.route("/books_title", methods=["POST"])
@login_required
def books_title():
    title=request.form.get("title")
    if db.execute("SELECT * FROM books WHERE (title = :title)", {"title":title}).rowcount==0:
        return render_template("error.html", message= "No matches with the title specified")
    books=db.execute("SELECT * FROM books WHERE (title=:title)", {"title": title})
    db.commit()
    return render_template("title.html", books=books)

#Specific book
@app.route("/books_title/<string:book_title>/<string:book_isbn>")
@login_required
def booktitle(book_title, book_isbn):
    """List details about a single book."""

    # Make sure flight exists.
    books=db.execute("SELECT * FROM books WHERE (title=:book_title)", {"book_title": book_title})
    reviews=db.execute("SELECT * FROM reviews WHERE (isbn_review=:book_isbn)", {"book_isbn": book_isbn})
    reviews_avg= db.execute ("SELECT round(avg(review::integer),1) as average , count(*) as count from reviews where (isbn_review =:book_isbn)", {"book_isbn": book_isbn})
    db.commit()
    return render_template("book.html", books=books, reviews=reviews, reviews_avg=reviews_avg)

#search by author
@app.route("/books_author", methods=["POST"])
@login_required
def books_author():
    author=request.form.get("author")
    author=author+'%'
    if db.execute("SELECT * FROM books WHERE (author similar to :author)", {"author":author}).rowcount==0:
        return render_template("error.html", message= "No matches with the ISBN specified")
    books=db.execute("SELECT * FROM books WHERE (author similar to :author)", {"author": author})
    db.commit()
    return render_template("author.html", books=books)

#Specific book
@app.route("/books_author/<string:book_author>/<string:book_isbn>")
@login_required
def bookauthor(book_author, book_isbn):
    """List details about a single book."""

    # Make sure flight exists.
    books=db.execute("SELECT * FROM books WHERE (author=:book_author) and (isbn=:book_isbn)", {"book_author": book_author, "book_isbn":book_isbn})
    reviews=db.execute("SELECT * FROM reviews WHERE (isbn_review=:book_isbn)", {"book_isbn": book_isbn})
    reviews_avg= db.execute ("SELECT round(avg(review::integer),1) as average, count(*) as count from reviews where (isbn_review =:book_isbn)", {"book_isbn": book_isbn})
    db.commit()
    return render_template("book.html", books=books, reviews=reviews, reviews_avg=reviews_avg)

#INSERT A REVIEW
@app.route("/review/<string:book_isbn>", methods=["POST", "GET"])
@login_required
def review(book_isbn):

    #Get information
    user1=session['user']
    book_review=request.form.get("review")
    opinion_review=request.form.get("opinion_review")
    if db.execute("SELECT * FROM reviews WHERE (username_review = :username) and (isbn_review = :isbn_review)", {"username":user1, "isbn_review":book_isbn}).rowcount>=1:
        return render_template("error.html", message="You can not make more than one review per book")

    db.execute("INSERT INTO reviews (isbn_review, review, username_review, review_opinion) VALUES (:book_isbn, :book_review, :user1, :opinion_review)",
            {"book_isbn": book_isbn, "book_review":book_review, "user1": user1, "opinion_review": opinion_review})
    db.commit()
    return render_template("review_success.html", message="Your review has been updated!") 

""" @app.route("/api/books/<book_isbn>")
def book_api(book_isbn):


    # Make sure flight exists.
    #books=db.execute("SELECT * FROM books WHERE (isbn=:book_isbn)", {"book_isbn": book_isbn})
    books= Book.query.get(book_isbn)

    #reviews_avg= db.execute ("SELECT round(avg(review::integer),1) as average, count(*) as count from reviews where (isbn_review =:book_isbn)", {"book_isbn": book_isbn})
    #db.commit()
    if books is None:
        return jsonify({"error": "Invalid book_isbn"}), 422
    
    return jsonify({
            "Author": books.author,
            "Title": books.title,
            "Year": books.year,
            "ISBN": books.isbn
        })

 """

 #=======================================================================