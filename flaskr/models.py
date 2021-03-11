import csv
import re
from datetime import datetime


from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy import and_

from flaskr import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(UserMixin, db.Model):
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(128), index=True)
    password = db.Column(db.String(128))
    updated_at = db.Column(db.DateTime, default=datetime.now())
    
    def __init__(self, userid, password):
        self.userid = userid
        self.password = generate_password_hash(password)
        
    def validate_password(self, password):
        return check_password_hash(self.password, password)
    
    def add_user(self):
        with db.session.begin(subtransactions=True):
            db.session.add(self)
        db.session.commit()
        
    @classmethod
    def select_by_userid(cls, userid):
        return cls.query.filter_by(userid=userid).first()
    
    def search_userid_by_id(id):
        """ Find userid using id """
        return db.session.query(User.userid).filter(User.id==id).first()
        
    def return_userid(id):
        """ Returns userid using id """
        user = re.sub("\\D", "", id)
        user = User.search_userid_by_id(user)
        user = text_extraction(str(user))
        return user
    
    def conformity_password(user, last_password):
        id = str(user)
        length = int(len(id))
        id = id[6:length-1]
        db_password = db.session.query(User.password).filter(User.id==id).first()
        db_password = password_extraction(str(db_password))
        # print(db_password)
        return check_password_hash(db_password, last_password)
   
    def change_password(user, password):
        new_password = generate_password_hash(password)
        user.password = new_password
        db.session.add(user)
        db.session.commit()
        
               
class Horse(db.Model):
    
    __tablename__ = 'feature_horses'
    
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.String(128), index=True, nullable=False)
    horsename = db.Column(db.String(128), index=True, nullable=False)
    comment = db.Column(db.String(1000))
    updated_at = db.Column(db.DateTime, default=datetime.now())
    
    def __init__(self, userid, horsename, comment):
        self.userid = userid
        self.horsename = horsename
        self.comment = comment
        
        
    def add_horse(self):
        with db.session.begin(subtransactions=True):
            db.session.add(self)
        db.session.commit()
        
    # def validata_distance(self, distance_start, distance_end):
    #     return self.distance_start <= self.distance_end
        
        
    def display_horse(userid):
        horses = db.session.query(Horse).filter(Horse.userid==userid).all()
        return horses
    
    def delete_horse(id):
        with db.session.begin(subtransactions=True):
            horse = db.session.query(Horse).filter(Horse.id==id).first()
            db.session.delete(horse)
        db.session.commit()
        
        
    def horse_search(dir, userid):
        list = []
        registered_horse = []
        horses = db.session.query(Horse.horsename).filter(Horse.userid==userid).all()
        for i in range(len(horses)):
            horse = text_extraction(str(horses[i]))
            registered_horse.append(horse)
        with open (dir, 'r') as f:
            reader = csv.reader(f)
            line = [row for row in reader]
            for i in range(1,len(line)):
                for j in range(len(registered_horse)):
                    if str(line[i][3]) == registered_horse[j]:
                        comment = db.session.query(Horse.comment).filter(and_(Horse.userid==userid, Horse.horsename==registered_horse[j])).first()
                        comment = text_extraction(str(comment))
                        line[i].append(comment)
                        list.append(line[i])                                      
        return list
    
    def search_comment(id):
        comment = db.session.query(Horse.comment).filter(Horse.id==id).first()
        comment = text_extraction(str(comment))
        return comment
    
    def search_horsename(id):
        horsename = db.session.query(Horse.horsename).filter(Horse.id==id).first()
        horsename = text_extraction(str(horsename))
        return horsename
    
    # def extract_comments():
    #     comment = db.session.query(Horse.comment).filter(and_(Horse.userid==userid, Horse.horsename==registered_horse[j])).first()
    #     comment = text_extraction(str(comment))
    #     return comment
    
    def horse_update_by_id(id, userid, horsename, comment):
        with db.session.begin(subtransactions=True):
            horse = Horse.query.get(id)
            horse.userid = userid
            horse.horsename = horsename
            horse.comment = comment
        db.session.commit()
                
        
def text_extraction(text):
    """ Extract only text when selecting from db """
    length = int(len(text))
    text = text[2:length-3]
    return text
    
def password_extraction(text):
    """ Extract only text when selecting from db """
    length = int(len(text))
    text = text[3:length-3]
    return text