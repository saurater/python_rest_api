#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python Rest API
Created on Tue May  3 08:46:40 2022
@author: Sam Faraday
"""
#Flask - a Microframework for web development
#request - to send requeststo a browser / app (get, post, update, put delete)
from flask import Flask, request
#creating an app by instatiating Flask
app = Flask(__name__)

""" -->       Part I - db Creation and Items adding     """
#Import SQLAlchemy to Manage Data 
from flask_sqlalchemy import SQLAlchemy

#Creating the database locally
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
#Stop Modifications warnings
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Creating our model (a table so to say)
class Books(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    name        = db.Column(db.String(80), unique=True, nullable = True)
    author      = db.Column(db.String(120))
    
    #this functions returns the table fields
    def __repr__(self):
        return f"{self.name} - {self.author}"
    
#Try creating the table
try:
    db.create_all()
except:
    print("Table has already been created")    

#Function to add the first books manually  
def add_books(book_name, book_author):
    db.session.add(Books(name=book_name, author=book_author))
    try:
        db.session.commit() 
    except:
        print("Error: This title has already been added" )  
        db.session.rollback() 
    return Books.query.all()
""" <--       Part I - db Creation and Items Adding     """

@app.route('/')
def index():
    return "Hello, Welcome to Flask API by Sam Faraday"
@app.route("/books")
def get_books():
    books = Books.query.all()
    output = []
    for book in books:
        book_data = {'id': book.id, 'name': book.name, 'author': book.author}
        output.append(book_data)
    return {"books": output}
@app.route("/books/<id>")
def get_book(id):
    book = Books.query.get_or_404(id)
    return {"name": book.name, "author": book.author}

@app.route("/books", methods=['POST'])
def add_book():
    book = Books(name=request.json['name'], author=request.json['author']) #Books(name="Karol3", author="Susy3")
    db.session.add(book)
    try:
        db.session.commit()
    except:
        return {'Error: name': book.name +  ' já existe'}
    return {'id': book.id}

@app.route('/books/<id>', methods=['DELETE'])
def delete_book(id):
    book = Books.query.get(id)
    if book is None:
        return {"error": "Book not found"}
    db.session.delete(book)
    db.session.commit()
    return {"message": "The book " + str(book) + " has been deleted" }
