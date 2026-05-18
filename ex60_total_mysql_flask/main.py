"""
create database bookstore_flask;

create table book(
    bookid int primary key auto_increment,
    bookname varchar(40) not null,
    publisher varchar(40),
    price int
);

create table customer(
    custid int primary key auto_increment,
    name varchar(40) not null,
    address varchar (40),
    phone varchar(30),
    password varchar(255) not null
);

create table orders(
    orderid int primary key auto_increment,
    custid int, bookid int, 
    saleprice int, orderdate date, 
    foreign key (custid) references customer(custid) on delete cascade,
    foreign key (bookid) references book(bookid) on delete cascade
); 
"""


import os

from flask import Flask, render_template, request, jsonify, session, url_for, redirect
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime 
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY')

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

def is_logged_in():
    return 'logged_in' in session
@app.route('/')
def index():
    if is_logged_in(): return redirect(url_for('books_page'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route('/register_page')
def register_page():
    return render_template('register.html')

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    hashed_pw = generate_password_hash(data['password'])
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO customer (name, address, phone, password) VALUES (%s, %s, %s, %s)", 
                (data['name'], data['address'], data['phone'], hashed_pw))
    mysql.connection.commit()
    cur.close()
    return jsonify({"success":True,"message":"회원가입 완료"})
    
@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM customer WHERE name = %s", [data['name']])
    user = cur.fetchone()
    cur.close()
    if user and check_password_hash(user['password'], data['password']):
        session['logged_in'] = True
        session['custid'] = user['custid']
        session['name'] = user['name']
        return jsonify({"success":True})
    return jsonify({"success":False, "message":"ID or PW 불일치"}), 401

@app.route('/books')
def books_page():
    if not is_logged_in(): return redirect(url_for('index'))
    return render_template('books.html')

@app.route('/add_book')
def add_books_page():
    if not is_logged_in(): return redirect(url_for('index'))
    return render_template('add_books.html')



@app.route('/api/books', methods=['GET'])
def api_get_books():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM book")
    books = cur.fetchall()
    cur.close()
    return jsonify(books)

@app.route('/api/order', methods=['POST'])
def api_order():
    data = request.get_json()
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO orders (custid, bookid, saleprice, orderdate) VALUES (%s, %s, %s, %s)",
                (session['custid'], data['bookid'], data['saleprice'], datetime.now().date()))
    mysql.connection.commit()
    cur.close()
    return jsonify({"success":True})

@app.route('/my_orders')
def my_order_page():
    if not is_logged_in(): return redirect(url_for('index'))
    return render_template('my_orders.html')

@app.route('/api/my_orders', methods=['GET'])
def api_get_orders():
    cur = mysql.connection.cursor()
    cur.execute("""
                SELECT *
                From orders o JOIN book b
                ON o.bookid = b.bookid
                where o.custid = %s
                """, [session['custid']])
    orders = cur.fetchall()
    cur.close()
    return jsonify(orders)
if __name__ == '__main__':
    app.run(debug=True, port=5000, host ='163.152.213.114')