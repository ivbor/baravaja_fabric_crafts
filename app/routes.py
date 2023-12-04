import json

from werkzeug.security import check_password_hash
from flask import render_template, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, login_required, \
    current_user, LoginManager

from .forms import LoginForm, RegisterForm
from .models import Good, User
from .app import app
from .routes_ext.route_language import get_user_language
from .routes_ext.route_cookie import set_cookie, render_with_cookies
from .routes_ext.route_admin import admin, edit, add, delete, \
    generate_password_hash, db


# user loading
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)
app.logger.info(f'new login {login_manager} successfully created')


@login_manager.user_loader
def load_user(user_id):
    app.logger.info(f'user {user_id} is being loaded')
    return User.query.get_or_404(user_id)


# before request
@app.before_request
def before_request():
    response = None
    if not request.cookies.get('user_language'):
        response = set_cookie(
            'user_language', get_user_language(app, request))
    if not current_user.is_authenticated:
        if request.cookies.get('logged_in'):
            if request.cookies['logged_in'] == 'true':
                if response:
                    response.set_cookie('logged_in', 'false')
                else:
                    response = set_cookie('logged_in', 'false')
    if response:
        rendered_template = render_template('index.html',
                                            request=request)

        response.set_data(rendered_template)
        return response


# serving static
@app.route('/favicon.ico/')
def get_icon():
    return app.send_static_file('images/logo/logo.png')


@app.route('/static/images/slides/<path:filename>')
def get_slide(filename):
    return app.send_static_file(f'images/slides/{filename}')


@app.route('/static/images/goods/<path:filename>')
def get_goods_photo(filename):
    return app.send_static_file(f'images/goods/{filename}')


@app.route('/static/scripts/<path:filename>')
def get_script(filename):
    return app.send_static_file(f'scripts/{filename}')


# general routes
@app.route('/index')
def index():
    app.logger.info('redirecting from /index to /home')
    return redirect(url_for('home'))


@app.route('/')
def root():
    app.logger.info('redirecting from / to /home')
    return redirect(url_for('home'))


@app.route('/<language>/')
@app.route('/home')
def home():
    language = request.cookies.get('user_language')
    app.logger.info('/home page loaded')
    return render_with_cookies('index.html')


@app.route('/<language>/')
@app.route('/login', methods=['GET', 'POST'])
def login():

    app.logger.info('loading /login')

    form = LoginForm()
    app.logger.info(f'form {form} is loaded')

    if request.method == 'POST' and form.validate_on_submit():

        app.logger.info('/login request method post')

        email = form.username.data
        app.logger.info(f'email is {email}')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(
                user.hashed_password, form.password.data):

            app.logger.info(f'user {user} is found, trying to log in')

            login_user(user)

            app.logger.info('Logged in successfully')

            return jsonify({'success': True})

        else:

            app.logger.info('Login failed. Please try again.')

            return jsonify({'success': False})

    app.logger.info('/login request method get')

    return render_with_cookies('login.html', form=form)


@app.route('/<language>/')
@app.route('/register', methods=['GET', 'POST'])
def register():
    app.logger.info('loading /register')

    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():

        app.logger.info('/register request method post')

        email = form.username.data
        app.logger.info(f'email is {email}')

        user = User.query.filter_by(email=email).first()

        if user:

            app.logger.info('User with this email exists already')

            return jsonify({'success': False, 'reason': 'email-exists'})

        if not check_password_hash(
                generate_password_hash(form.password.data),
                form.repeat_password.data):

            return jsonify({'success': False, 'reason': 'unmatched'})

        new_user = \
            User(email=form.username.data,
                 hashed_password=generate_password_hash(form.password.data))

        db.db.session.add(new_user)

        db.db.session.commit()

        return redirect(url_for('login'))

    return render_with_cookies('register.html', form=form)


@app.route('/<language>/')
@app.route('/shop')
def shop():
    app.logger.info('loading /shop')
    goods = Good.query.all()
    return render_with_cookies('shop.html')


@app.route('/<language>/')
@app.route('/restore')
def restore():
    app.logger.info('loading /restore')
    return render_with_cookies('restore.html')


# login required routes
@app.route('/<language>/')
@app.route('/cart')
@login_required
def cart():
    app.logger.info('loading /cart')
    return render_with_cookies('cart.html')


@app.route('/<language>/')
@app.route('/logout')
@login_required
def logout():
    app.logger.info('loading /logout')
    logout_user()
    app.logger.info('user {current_user} logged out')
    return set_cookie('logged_in', 'False')


@app.route('/add_to_cart/<int:good_id>')
@login_required
def add_to_cart(good_id):
    app.logger.info('loading /add_to_cart')
    good = Good.query.get_or_404(good_id)

    if good:
        app.logger.info(f'good {good_id} found')

        if 'cart' not in request.cookies.keys():
            app.logger.info('nothing is in the cart')
            set_cookie('cart', '')

        cart_dict = json.loads(request.cookies['cart'])
        app.logger.info(f'cart_dict: {cart_dict}')

        if str(good_id) not in cart_dict.keys():
            app.logger.info(f'no {good_id} in the cart')
            cart_dict[str(good_id)] = 1
            set_cookie('cart', str(cart_dict))
            app.logger.info(f'good {good_id} added to the cart')
        else:
            app.logger.info(f'{good_id} in the cart' +
                            f' with amount {cart_dict[str(good_id)]}')
            cart_dict[str(good_id)] += 1
            set_cookie('cart', str(cart_dict))
            app.logger.info(f'good {good_id} added to the cart')


@app.route('/cart')
@login_required
def view_cart():
    return render_with_cookies('cart.html')
