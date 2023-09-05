from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    app.app_context().push()
    db.init_app(app)
    
class User(db.Model):
    """User model"""
    
    __tablename__ = 'users'
    
    username = db.Column(db.String(20),
                         primary_key=True,
                         unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    
    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        password = bcrypt.generate_password_hash(pwd)
        pwd_hash_utf8 = password.decode('utf8')
        
        return cls(username=username, password=pwd_hash_utf8, email=email, first_name=first_name, last_name=last_name)
    
    @classmethod
    def authentication(cls, username, password):
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password,password):
            return user
        else:
            return False
        
class Feedback(db.Model):
    __tablename__ = 'feedbacks'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String, db.ForeignKey('users.username', ondelete='CASCADE'))
    user = db.relationship('User', backref='feedbacks')
    
    @classmethod
    def new_feed(cls, title,content, username):
        """create new feedback instance"""
        return cls(title=title, content=content, username=username)
    
    def update_feed(self, title, content):
        self.title = title
        self.content = content
        
        db.session.commit()
        return self