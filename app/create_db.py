from models import *


user = User.query.filter_by(email='onwuzulikee1@gmail.com')
db.session.delete(user)
db.session.commit()