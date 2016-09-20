from models import db, User

db.create_all()

user = User('onwuzulike','emeka',)
db.session.add(user)
db.session.commit()