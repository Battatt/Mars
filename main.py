from flask import Flask, render_template, redirect, abort, request
from data import db_session
from data.jobs import Jobs
from data.users import User
from forms.users import RegisterForm
from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from forms.login_form import LoginForm
from forms.jobs_form import JobsForm
from forms.departs_form import DepartmentForm
from data.departments import Departament
from data.category import Category
from forms.category_form import CategoryForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
@app.route('/<title>')
@app.route('/index/<title>')
def index(title="Колонизация Марса"):
    db_sess = db_session.create_session()
    works = db_sess.query(Jobs).all()
    return render_template("works_list.html", title=title, works_list=works)


@app.route("/training/<prof>")
def second_index(prof):
    if 'ИНЖЕНЕР' in prof.upper() or 'СТРОИТЕЛ' in prof.upper():
        prof = 0
    else:
        prof = 1
    return render_template('prof.html', prof=prof, title="Профессия")


@app.route("/list_prof/")
@app.route("/list_prof/<list>")
def list_index(list="ul"):
    l_type = 0 if list == 'ul' else 1 if list == 'ol' else -1
    professions = [
        'инженер-исследователь', 'пилот', 'строитель', 'экзобиолог', 'врач', 'инженер по терраформированию',
        'климатолог', 'специалист по радиационной защите', 'астрогеолог', 'гляциолог', 'инженер жизнеобеспечения',
        'метеоролог', 'оператор марсохода', 'киберинженер', 'штурман', 'пилот дронов'
    ]
    return render_template('list_prof.html', list_type=l_type, profs=professions)


@app.route("/answer")
@app.route("/auto_answer")
def auto_asnwer():
    params = {}
    params['title'] = "Анкета"
    params["surname"] = "Watny"
    params["name"] = "Mark"
    params["education"] = "выше среднего"
    params["profession"] = "штурман марсохода"
    params["sex"] = "male"
    params["motivation"] = "Всегда хотел застрять на Марсе!"
    params["ready"] = True
    return render_template("auto_answer.html", **params)


@app.route("/distribution")
def rooms(peoples=None):
    if peoples is None:
        peoples = ["Пётр", "Алексей", "Михаил", "Павел", "Николай", "Александр"]
    return render_template("rooms.html", peoples=peoples, title="По Каютам!")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            surname=form.surname.data,
            name=form.name.data,
            email=form.email.data,
            age=form.age.data,
            position=form.position.data,
            speciality=form.speciality.data,
            address=form.address.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


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


@app.route('/jobs',  methods=['GET', 'POST'])
@login_required
def add_jobs():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        cats = [i.id for i in db_sess.query(Category).all()]
        if form.category.data:
            if form.category.data not in cats:
                abort(404)
        else:
            abort(404)
        jobs = Jobs()
        jobs.team_leader = form.team_leader.data
        jobs.job = form.job.data
        jobs.work_size = form.work_size.data
        jobs.collaborators = form.collaborators.data
        jobs.category = form.category.data
        jobs.is_finished = form.is_finished.data
        if jobs.is_finished is False:
            jobs.end_date = None
        db_sess.add(jobs)
        db_sess.commit()
        return redirect('/')
    return render_template('jobs.html', title='Adding a Job',
                           form=form)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = JobsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id).first()
        flag = jobs.team_leader == current_user.id or current_user.id == 1
        if jobs and flag:
            form.team_leader.data = jobs.team_leader
            form.job.data = jobs.job
            form.work_size.data = jobs.work_size
            form.category.data = jobs.category
            form.collaborators.data = jobs.collaborators
            form.is_finished.data = jobs.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id).first()
        flag = jobs.team_leader == current_user.id or current_user.id == 1
        cats = [i.id for i in db_sess.query(Category).all()]
        if form.category.data:
            if form.category.data not in cats:
                abort(404)
        if jobs and flag:
            jobs.team_leader = form.team_leader.data
            jobs.job = form.job.data
            jobs.work_size = form.work_size.data
            jobs.collaborators = form.collaborators.data
            jobs.category = form.category.data
            jobs.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('jobs.html',
                           title='Job Edit',
                           form=form
                           )


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id).first()
    flag = jobs.team_leader == current_user.id or current_user.id == 1
    if jobs and flag:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route("/departments")
def departments_list():
    db_sess = db_session.create_session()
    departs = db_sess.query(Departament).all()
    return render_template("departs.html", title="Departments", departs=departs)


@app.route('/add_depart',  methods=['GET', 'POST'])
@login_required
def add_depart():
    form = DepartmentForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        depart = Departament()
        depart.title = form.title.data
        depart.chief = form.chief.data
        depart.members = form.members.data
        depart.email = form.email.data
        db_sess.add(depart)
        db_sess.commit()
        return redirect('/departments')
    return render_template('add_depart.html', title='Adding a Department',
                           form=form)


@app.route('/departments/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_depart(id):
    form = DepartmentForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        depart = db_sess.query(Departament).filter(Departament.id == id).first()
        flag = depart.chief == current_user.id or current_user.id == 1
        if depart and flag:
            form.chief.data = depart.chief
            form.title.data = depart.title
            form.members.data = depart.members
            form.email.data = depart.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        depart = db_sess.query(Departament).filter(Departament.id == id).first()
        flag = depart.chief == current_user.id or current_user.id == 1
        if depart and flag:
            depart.chief = form.chief.data
            depart.title= form.title.data
            depart.members = form.members.data
            depart.email = form.email.data
            db_sess.commit()
            return redirect('/departments')
        else:
            abort(404)
    return render_template('add_depart.html',
                           title='Department Edit',
                           form=form
                           )

@app.route('/departments_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def depart_delete(id):
    db_sess = db_session.create_session()
    depart = db_sess.query(Departament).filter(Departament.id == id).first()
    flag = depart.chief == current_user.id or current_user.id == 1
    if depart and flag:
        db_sess.delete(depart)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/departments')


@app.route("/category")
def categories():
    db_sess = db_session.create_session()
    cats = db_sess.query(Category).all()
    return render_template("categories.html", title="Categories", categories=cats)


@app.route('/add_category',  methods=['GET', 'POST'])
@login_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        cat = Category()
        cat.name = form.name.data
        db_sess.add(cat)
        db_sess.commit()
        return redirect('/category')
    return render_template('cats.html', title='Adding a Category',
                           form=form)


@app.route('/category/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    form = CategoryForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        cat = db_sess.query(Category).filter(Category.id == id).first()
        if cat:
            form.name.data = cat.name
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        cat = db_sess.query(Category).filter(Category.id == id).first()
        if cat:
            cat.name = form.name.data
            db_sess.commit()
            return redirect('/categories')
        else:
            abort(404)
    return render_template('cats.html',
                           title='Category Edit',
                           form=form
                           )


@app.route('/category_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def category_delete(id):
    db_sess = db_session.create_session()
    cat = db_sess.query(Category).filter(Category.id == id).first()
    if cat:
        db_sess.delete(cat)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/categories')


if __name__ == '__main__':
    db_session.global_init("db/mars_explorer.db")
    app.run(port=5000, host='127.0.0.1')
