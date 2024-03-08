from flask import Flask, render_template, redirect, request, make_response
from forms.login_form_old import LoginForm, SuperSpecialForm
from data import db_session
from data.jobs import Jobs
from data.users import User
from forms.users import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


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


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        f = [form.astro_id.data, form.astro_password.data, form.captain_id.data, form.captain_password.data]
        return redirect('/success')
    return render_template('login.html', title='Авторизация', form=form)


@app.route("/success", methods=['GET', 'POST'])
def success():
    form = SuperSpecialForm()
    if form.validate_on_submit():
        return redirect("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return render_template("supersubmit.html", title="Yes?", form=form)


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


@app.route("/cookie_test")
def cookie_test():
    visits_count = int(request.cookies.get("visits_count", 0))
    if visits_count:
        res = make_response(
            f"Вы пришли на эту страницу {visits_count + 1} раз")
        res.set_cookie("visits_count", str(visits_count + 1),
                       max_age=60 * 60 * 24 * 365 * 2)
    else:
        res = make_response(
            "Вы пришли на эту страницу в первый раз за последние 2 года")
        res.set_cookie("visits_count", '1',
                       max_age=60 * 60 * 24 * 365 * 2)
    return res


if __name__ == '__main__':
    db_session.global_init("db/mars_explorer.db")
    app.run(port=5000, host='127.0.0.1')
