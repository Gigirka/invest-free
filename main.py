import os
import sqlite3

from io import BytesIO
from flask import Flask, render_template, redirect, make_response, jsonify, request, send_file
from werkzeug.utils import secure_filename

from data import db_session
from data.api import jobs_api, users_resource
from data.forms.login import LoginForm
from data.forms.user import InvestorRegisterForm, BusinessmanRegisterForm
from flask_login import LoginManager, login_user, login_required, logout_user
from data.jobs import Jobs
from data.users import User
from data.forms.add_job import AddJobForm
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

db_session.global_init("db/mars.db")


@app.route('/')
def index():
    db_sess = db_session.create_session()
    # context = {}
    # context["jobs"] = db_sess.query(Jobs).all()
    return render_template('index.html')  # **content


@app.route('/register-invest', methods=['GET', 'POST'])
def reqister_invest():
    form = InvestorRegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register-invest.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register-invest.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            type='investor',
            name=form.name.data,
            email=form.email.data,
            age=form.age.data,
            speciality=form.speciality.data,
            address=form.address.data,
            capital=form.capital.data,
            exp=form.exp.data,
            personal=form.personal.data,
            qualification=form.qualification.data,
            private_or_fund=form.private_or_fund.data,
            password=form.password.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register-invest.html', title='Регистрация', form=form)


@app.route('/register-business', methods=['GET', 'POST'])
def reqister_business():
    form = BusinessmanRegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register-business.html', title='Регистрация', form=form,
                                   message='Пароли не совпадают')
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register-business.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            type='businessman',
            company_name=form.company_name.data,
            email=form.email.data,
            money=form.money.data,
            password=form.password.data,
            staff=form.staff.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register-business.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/add_job', methods=['GET', 'POST'])
@login_required
def add_job():
    global job_data
    global owner_data
    global work_size_data
    global collaborators_data
    add_form = AddJobForm()
    if add_form.validate_on_submit():
        job_data = add_form.job.data,
        owner_data = add_form.owner.data,
        work_size_data = add_form.work_size.data,
        collaborators_data = add_form.collaborators.data

        return redirect("/add_image")
    return render_template('add_job.html', title='Добавление работы',
                           form=add_form)


@app.route('/add_image', methods=['GET', 'POST'])
@login_required
def add_image():
    global job_data
    global owner_data
    global work_size_data
    global collaborators_data
    # print(job_data, owner_data, work_size_data, collaborators_data)
    # print(request.form)
    # add_form = AddJobForm()
    # if add_form.validate_on_submit():
    #     db_sess = db_session.create_session()
    #     # print(add_form.image.file)
    #     # filename = secure_filename(add_form.image.file.filename)
    #     # file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    #     # form.fileName.file.save(file_path)
    #     # print(add_form.image.data)
    #     # print(request.files)
    #     # file = request.form['file']
    #     # print(file)
    #     # f = open(add_form.image.data, 'rb')
    #     # print(f)
    #     # print(add_form.image.read())
    #     # room_image = request.files
    #     # print(room_image)
    #     # img_name = add_form.image.data
    #     # print(img_name)
    #     # product_img = readImage(img_name)
    #     # print(product_img)
    #     # product_img_binary = sqlite3.Binary(product_img)
    #     jobs = Jobs(job=job_data,
    #                 owner=owner_data,
    #                 work_size=work_size_data,
    #                 collaborators=collaborators_data)
    #     # image=add_form.image.data)
    #     # is_finished=add_form.is_finished.data)
    #     db_sess.add(jobs)
    #     db_sess.commit()
    return render_template('add_image.html')
    # return render_template('add_image.html', title='Добавление работы',
    #                        form=add_form)


@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        print(f)
        a = open(f.filename, 'rb')
        print(a)
        f.save(f.filename)
        return redirect("/")


def readImage(img_name):
    try:
        fin = open(img_name, 'rb')
        img = fin.read()
        return img
    except:
        print("ERROR!!")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


if __name__ == '__main__':
    app.register_blueprint(jobs_api.blueprint)
    # для списка объектов
    api.add_resource(users_resource.UsersListResource, '/api/v2/users')

    # для одного объекта
    api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:users_id>')
    app.run(port=8183, host='127.0.0.1')
