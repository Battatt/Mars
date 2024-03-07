from data import db_session
from data.users import User
from data.jobs import Jobs

#  db_name = input()
db_session.global_init("db/mars_explorer.db")
db_sess = db_session.create_session()
maxes = max([len(job.collaborators.split(', ')) for job in db_sess.query(Jobs).all()])
team_leaders = [job.team_leader for job in db_sess.query(Jobs).all()]
flager = {}
res = []
for i in team_leaders:
    flager[i] = db_sess.query(Jobs).filter(Jobs.team_leader == i).first().collaborators
for i in flager.keys():
    print(flager[i].split(', '))
    if len(flager[i].split(', ')) == maxes:
        res.append(db_sess.query(User).filter(User.id == i).first().surname + ' ' +
                   db_sess.query(User).filter(User.id == i).first().name)
print(*res, sep='\n')
