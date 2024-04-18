import io
import sqlite3
from PIL import Image, ImageDraw
from flask import Flask, render_template, redirect, make_response, jsonify, send_file, request
from data import db_session
from data.api import jobs_api, users_resource
from data.forms.login import LoginForm
from data.forms.user import InvestorRegisterForm, BusinessmanRegisterForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
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
    # conn = sqlite3.connect("db/mars.db")
    # cursor = conn.cursor()
    # cursor.execute("SELECT * FROM jobs WHERE user_id=?", (current_user.id,))
    # your_projects = cursor.fetchall()
    # conn.close()
    # for i in range(len(your_projects)):
    #     your_projects[i] = list(your_projects[i])
    try:
        your_projects = db_sess.query(Jobs).filter(Jobs.user_id == current_user.id).all()
    except:
        your_projects = []
    if your_projects:
        context["your_projects"] = your_projects
    return render_template('index.html', **context)  # **content


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
        image_file = form.image.data
        if image_file:
            image_data = image_file.read()
        else:
            image_data = None
        user = User(
            type='investor',
            name=form.name.data,
            email=form.email.data,
            image=image_data,
            capital=form.capital.data,
            personal=form.personal.data,
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
        image_file = form.image.data
        if image_file:
            image_data = image_file.read()
        else:
            image_data = None
        user = User(
            type='businessman',
            email=form.email.data,
            password=form.password.data,
            image=image_data
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

        image_file = add_form.image.data
        if image_file:
            image_data = image_file.read()
        else:
            image_data = None
        jobs = Jobs(project_name=add_form.project_name.data,
                    info=add_form.info.data,
                    work_size=add_form.work_size.data,
                    image=image_data,
                    user_id=current_user.id,
                    needed_money=add_form.needed_money.data)
        # is_finished=add_form.is_finished.data)
        db_sess.add(jobs)
        db_sess.commit()
        return redirect("/")
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


def get_profile_picture():
    conn = sqlite3.connect("db/mars.db")
    cursor = conn.cursor()
    user_id = current_user.id
    cursor.execute("SELECT image FROM users WHERE id=?", (user_id,))
    image_data = cursor.fetchone()[0]
    conn.close()

    if image_data:  # Преобразование изображения в круг
        try:
            image = Image.open(io.BytesIO(image_data))

            width, height = image.size
            size = min(width, height)
            left = (width - size) / 2
            top = (height - size) / 2
            right = (width + size) / 2
            bottom = (height + size) / 2
            image = image.crop((left, top, right, bottom))

            mask = Image.new('L', image.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((0, 0) + image.size, fill=255)
            image.putalpha(mask)
            output = io.BytesIO()
            image.save(output, format='PNG')
            output.seek(0)

            return send_file(output, mimetype='image/png')

        except Exception as e:
            # изображение по умолчанию
            return send_file('static/img/default-profile-image.jpg', mimetype='image/jpeg')

    else:
        # Возвращаем изображение по умолчанию
        return send_file('static/img/default-profile-image.jpg', mimetype='image/jpeg')


@app.route('/profile_picture')
def get_profile_picture_route():
    return get_profile_picture()


def get_project_picture(project_id):
    conn = sqlite3.connect("db/mars.db")
    cursor = conn.cursor()
    cursor.execute("SELECT image FROM jobs WHERE id=?", (project_id,))
    image_data = cursor.fetchone()[0]
    conn.close()
    if image_data:
        image = Image.open(io.BytesIO(image_data))
        output = io.BytesIO()
        image.save(output, format='PNG')
        output.seek(0)
        return send_file(output, mimetype='image/png')
    else:
        # Возвращаем изображение по умолчанию
        return send_file('static/img/default-profile-image.jpg', mimetype='image/jpeg')


@app.route('/project_picture/<int:project_id>')
def get_project_picture_route(project_id):
    return get_project_picture(project_id)


project = {}


@app.route('/open-project/<int:project_id>', methods=['GET', 'POST'])
def open_project(project_id):
    global project
    conn = sqlite3.connect("db/mars.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs WHERE id=?", (project_id,))
    project_data = cursor.fetchone()
    conn.close()

    conn = sqlite3.connect("db/mars.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM users WHERE id=?", (project_data[3],))
    name = cursor.fetchall()
    conn.close()

    project = {
        'id': project_data[0],
        'project_name': project_data[1],
        'work_size': project_data[2],
        'date': project_data[6],
        'info': project_data[5],
        'needed_money': project_data[7],
        'invested_money': project_data[8],
        'author': name[0][0]
    }
    return render_template('open-project.html', title='Страница проекта', project=project)


@app.route('/invest', methods=['GET', 'POST'])
def invest():
    global project
    print(project['invested_money'])
    try:
        money = request.form["text"]
        conn = sqlite3.connect("db/mars.db")
        cursor = conn.cursor()
        cursor.execute(
            f"UPDATE jobs SET invested_money = invested_money + {money}  WHERE id={project["id"]}").fetchone()
        project['invested_money'] = int(project['invested_money']) + int(money)
        cursor.execute(f"UPDATE users SET money = money - {money}  WHERE id={current_user.id}").fetchone()
        conn.commit()
        conn.close()
        print(project['invested_money'])
        return render_template('open-project.html', title='Страница проекта', project=project)
    except:
        return render_template('open-project.html', title='Страница проекта', project=project)


if __name__ == '__main__':
    app.register_blueprint(jobs_api.blueprint)
    # для списка объектов
    api.add_resource(users_resource.UsersListResource, '/api/v2/users')

    # для одного объекта
    api.add_resource(users_resource.UsersResource, '/api/v2/users/<int:users_id>')
    app.run(port=8185, host='127.0.0.1')
