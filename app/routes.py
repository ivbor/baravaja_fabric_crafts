from flask import Flask, render_template, send_from_directory, redirect, \
    url_for, request, flash, session
from flask_login import login_user, logout_user, login_required
from .models import Good, Order, User, db

app = Flask('app')


@app.route('/')
def index():
    return redirect(url_for('home'))


@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('app/templates/styles', filename)


@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.password == request.form['password']:
            login_user(user)
            flash('Logged in successfully', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login failed. Please try again.', 'danger')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/add_to_cart/<int:good_id>')
@login_required
def add_to_cart(good_id):
    good = Good.query.get(good_id)
    if good:
        if 'cart' not in session:
            session['cart'] = []
        session['cart'].append(good_id)
        flash('Good added to cart', 'success')
    return redirect(url_for('index'))


@app.route('/cart')
@login_required
def view_cart():
    cart_items = []
    if 'cart' in session:
        cart_items = [Good.query.get(good_id)
                      for good_id in session['cart']]
    return render_template('cart.html', cart_items=cart_items)
