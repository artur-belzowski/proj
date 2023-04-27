from flask import Flask
from flask import render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask import session
# import requests
# import json
from collection import Collection
from get_nft_data import get_nft_data

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'nbiwbfui98523h8we34ty98wt8w#$%@MN$#NBJ^%$#@HBB'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        user = User.query.filter_by(username=username).first()
        if user:
            message = 'Użytkownik o takiej nazwie już istnieje.'
            return render_template('register.html', message=message)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    collections = Collection.get_collections()
    change24 = collections[0].change24
    reward_points = collections[0].reward_points
    floor_price = collections[0].floor_price
    return render_template('index.html', collections=collections, change24=change24, reward_points=reward_points, floor_price=floor_price)


@app.route('/<collection_name>/')
def floor_price(collection_name):
    nft_data = get_nft_data(collection_name)
    return render_template('collection.html', collection_name=collection_name, nft_data=nft_data)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = db.session.query(User.id).filter_by(username=username).first()
        if user:
            session['user_id'] = user[0]  # zapisanie ID użytkownika do sesji
            return redirect(url_for('index'))
        else:
            error = 'Nieprawidłowa nazwa użytkownika lub hasło'
            return render_template('login.html', error=error)
    else:
        return render_template('login.html')


@app.before_request
def before_request():
    if 'user_id' not in session and request.endpoint not in ['login', 'register', 'index', 'collection', 'logout']:
        return redirect(url_for('login'))


@app.route('/logout/', methods=['POST'])
def logout():
    session.pop('user_id', None)  # usuwanie sesji
    return redirect(url_for('login'))


# @app.route('/dashboard')
# def dashboard():
#     user_id = session.get('user_id')
#     if user_id:
#         user = User.query.filter_by(id=user_id).first()
#         if user:
#             return render_template('dashboard.html', user=user)
#         else:
#             session.pop('user_id', None)  # usuwanie sesji, jeśli nie znaleziono użytkownika
#             return redirect(url_for('login'))
#     else:
#         return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
