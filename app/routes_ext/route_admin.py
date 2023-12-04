import subprocess

from werkzeug.security import generate_password_hash
from functools import wraps
from flask import abort
from flask_login import AnonymousUserMixin

from app.app import os, db
from app.models import Order
from app.forms import obj_map, DeleteForm
from app.routes import redirect, request, url_for, render_with_cookies, \
    current_user, login_required, Good, User, app


def admin_required(func):

    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not isinstance(current_user, AnonymousUserMixin):
            if not current_user.is_admin:
                app.logger.info(
                    f'current_user is {current_user} and not admin')
                abort(403)
        else:
            app.logger.info(
                f'current_user is {current_user} and not admin')
            abort(403)

        return func(*args, **kwargs)

    return decorated_view


@app.route('/admin')
@admin_required
@login_required
def admin():
    app.logger.info('loading /admin')
    users = User.query.all()
    goods = Good.query.all()
    orders = Order.query.all()
    return render_with_cookies('admin.html',
                               users=users,
                               orders=orders,
                               goods=goods)


@app.route('/edit_<obj>/<int:obj_id>', methods=['GET', 'POST'])
@admin_required
@login_required
def edit(obj, obj_id):
    app.logger.info('loading /edit')

    obj_instance = obj_map[obj][1].query.get_or_404(obj_id)
    app.logger.info(f'{obj_instance} found')

    form = obj_map[obj][0](obj=obj_instance)
    app.logger.info(f'form {form} loaded')

    if request.method == 'POST' and form.validate_on_submit():
        app.logger.info('/edit request method post')
        # if is has not changed or available
        if (not obj_map[obj][1].query.get(form.id.data)) or \
                form.id.data == obj_id:
            form.populate_obj(obj_instance)
            app.logger.info('{obj_instance} populated')
            db.db.session.commit()
            app.logger.info('changes committed to the db')
        else:
            app.logger.info(f'id {obj_id} for {obj} is unavailable')
            return redirect(url_for('edit', obj=obj, obj_id=obj_id))
        return redirect(url_for('admin'))

    return render_with_cookies('edit.html', form=form, obj=obj, add=False)


@app.route('/add_<obj>', methods=['GET', 'POST'])
@admin_required
@login_required
def add(obj):
    app.logger.info('loading /add')

    form = obj_map[obj][0]()
    app.logger.info(f'form {form} loaded')

    objs = obj_map[obj][1].query.all()
    new_id = len(objs) + 1
    form.id.data = new_id

    if request.method == 'POST' and form.validate_on_submit():

        app.logger.info('/add request method post')

        # check if all required ids are available
        # so that server would not go down
        # if mistake is made when adding some info manually
        # and fill all mandatory fields in advance

        if obj == 'user':
            new_obj = obj_map[obj][1](
                email=form.email.data,
                hashed_password=generate_password_hash(form.password.data))

        elif obj == 'order':

            max_user_id = len(User.query.all())
            user_id = form.user_id.data
            if user_id < 0 or user_id > max_user_id:
                return redirect(url_for('add', obj=obj))

            new_obj = obj_map[obj][1](
                user_id=form.user_id.data,
                summ=form.summ.data,
                contents=form.contents.data,
                datetime=form.datetime.data)

        elif obj == 'good':

            photos = form.photos.data.split(' ')
            for photo in photos:
                if not os.path.isfile(os.getcwd() +
                                      '/app/static/images/goods/' + photo):
                    return redirect(url_for('add', obj=obj))

            new_obj = obj_map[obj][1](
                name=form.name.data,
                price=form.price.data,
                description=form.description.data)

        # if id is available
        if not obj_map[obj][1].query.get(form.id.data):
            form.populate_obj(new_obj)
            app.logger.info('{obj_instance} populated')
            db.db.session.add(new_obj)
            db.db.session.commit()
            app.logger.info('changes committed to the db')
        return redirect(url_for('admin'))

    return render_with_cookies('edit.html', form=form, obj=obj, add=True)


@app.route('/delete_<obj>/<int:obj_id>', methods=['GET', 'POST'])
@admin_required
@login_required
def delete(obj, obj_id):
    obj_instance = obj_map[obj][1].query.get_or_404(obj_id)

    form = DeleteForm()

    if request.method == 'POST' and form.validate_on_submit():
        try:
            db.db.session.delete(obj_instance)
            db.db.session.commit()
            return redirect(url_for('admin'))
        except Exception as e:
            db.db.session.rollback()
            app.logger.info(
                "An error occurred while deleting the user." +
                f"Error: {str(e)}")

    return render_with_cookies('delete.html',
                               obj=obj, obj_id=obj_id, form=form)


@app.route('/sync_to_file')
@login_required
@admin_required
def sync_to_file():
    try:
        subprocess.run(['pg_dump',
                        '-U', app.config['SQLALCHEMY_DATABASE_URI']
                        .split('@')[0].split('/')[-1],
                        '-d', app.config['SQLALCHEMY_DATABASE_URI']
                        .split('@')[0].split('/')[-1],
                        '-f', os.getcwd() + '/backup.dump'])
    except Exception as e:
        app.logger.info(f'Error synchronizing: {str(e)}')
    return redirect(url_for('admin'))


@app.route('/sync_from_file')
@login_required
@admin_required
def sync_from_file():

    from sqlalchemy import create_engine

    db.db.session.remove()
    del db.db
    db_name = app.config['SQLALCHEMY_DATABASE_URI'].split(
        '@')[0].split('/')[-1]
    db_user = app.config['SQLALCHEMY_DATABASE_URI'].split('/')[-1]
    engine = create_engine(
        app.config['SQLALCHEMY_DATABASE_URI'][:-len(db_name)])
    # check if app still has an active connection to the database
    app.logger.info(f'engine: {engine}')
    conn = engine.connect()
    conn.execute(f'DROP DATABASE IF EXISTS {db_name};')
    conn.close()
    engine.dispose()

    subprocess.run(['psql', '-U', db_user, '-d', db_name,
                    '-f', os.getcwd() + '/backup.dump'])

    db.db.init_app(app)
    db.db.create_all()

    return redirect(url_for('admin'))
