from models import *

db.create_all()

user = User.query.filter_by(email='onwuzulikee1@gmail.com')
db.session.delete(user)
db.session.commit()