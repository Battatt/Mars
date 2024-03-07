from flask import Flask, render_template


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


if __name__ == '__main__':
    app.run(port=5000, host='127.0.0.1')
