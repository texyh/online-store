from models import *

db.create_all()

user = User('admin','admin@example.com','emmanuel11',True)
#profile = Profile('08064715300','male','2016-08-5','2016-08-5','ABU Zaria','1')
db.session.add(user)
db.session.commit()

print ('added admin')