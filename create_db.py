from models import *

db.create_all()

user = User('admin','admin@example.com','emmanuel11',True)

market = Market()
db.session.add(user)
db.session.commit()
