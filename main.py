from flask import Flask, render_template, redirect
from login_form import LoginForm, SuperSpecialForm
from data import db_session
from data.users import User
import sqlalchemy
from data.jobs import Jobs

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/')
@app.route('/<title>')
@app.route('/index/<title>')
def index(title="Колонизация Марса"):
    return render_template("base.html", title=title)


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


def add_user(surname, name, age, position, speciality, address, email):
    try:
        user = User()
        user.surname = surname
        user.name = name
        user.age = age
        user.position = position
        user.speciality = speciality
        user.address = address
        user.email = email
        db_sess = db_session.create_session()
        db_sess.add(user)
        db_sess.commit()
    except sqlalchemy.exc.IntegrityError as e:
        print("Такой e-mail уже есть")


if __name__ == '__main__':
    db_session.global_init("db/mars_explorer.db")
    if input("Введите пустую строку чтобы не вводить изменения в БД:"):
        add_user("Scott", "Ridley", 21, "captain",
                 "research engineer", "module 1", "scott_chief@mars.org")
        add_user("Mark", "Smith", 34, "researcher",
                 "research engineer", "module 3 block A", "mark228@mars.org")
        add_user("Bob", "Rock", 42, "builder",
                 "engineer", "module -1 block D", "builders_corp1@mars.org")
        add_user("Bill", "Fest", 37, "builder",
                 "Rock sider", "module -4 block C", "builders_corp2@mars.org")
        add_user("Jim", "Eier", 22, "builder",
                 "Constructor", "module 3 block F", "main_builders_corp@mars.org")
    app.run(port=5000, host='127.0.0.1')
