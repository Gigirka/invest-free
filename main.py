from flask import Flask, render_template, redirect, make_response, jsonify
from data import db_session
from data.api import jobs_api, users_resource
from data.forms.login import LoginForm
from data.forms.user import RegisterForm
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
    context = {}
    context["jobs"] = db_sess.query(Jobs).all()
    return render_template('index.html', **context)


@app.route('/register-invest', methods=['GET', 'POST'])
def reqister_invest():
    form = RegisterForm()
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
            surname=form.name.data,
            name=form.name.data,
            email=form.email.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register-invest.html', title='Регистрация', form=form)


@app.route('/register-business', methods=['GET', 'POST'])
def reqister_business():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register-business.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register-business.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.name.data,
            name=form.name.data,
            email=form.email.data,
            age=form.age.data,
            # position=form.position.data,
            # speciality=form.speciality.data,
            # address=form.address.data
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
    add_form = AddJobForm()
    if add_form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = Jobs(job=add_form.job.data,
                    team_leader=add_form.team_leader.data,
                    work_size=add_form.work_size.data,
                    collaborators=add_form.collaborators.data,
                    is_finished=add_form.is_finished.data)
        db_sess.add(jobs)
        db_sess.commit()
        return redirect('/')
    return render_template('add_job.html', title='Добавление работы',
                           form=add_form)


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
