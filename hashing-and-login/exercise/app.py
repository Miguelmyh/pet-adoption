from flask import Flask, redirect, render_template, session, flash
from models import db, connect_db, User, Feedback
from forms import UserRegistrationForm, UserLoginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)

app.config['SECRET_KEY'] = '123'
app.config['DEBUG_TB_ENABLED'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///twitter_db'
app.config['SQLALCHEMY_ECHO'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
# db.create_all()

@app.route('/')
def redir_register():
    """redirect to the register page"""
    if 'username' in session:
        username = session['username']
        return redirect(f'/users/{username}')
    return redirect('/register')

@app.route('/users/<username>')
def show_secret(username):
    feedbacks = Feedback.query.all()
    user = User.query.get(username)
    if 'username' not in session:
        flash('please login first', 'danger')
        return redirect('/login')
    if user.username == session['username']:
    
        return render_template('user_details.html', user=user, feedbacks=feedbacks)
    else:
        flash('Invalid username', 'danger')
        actual_user = session['username']
        return redirect(f'/users/{actual_user}')
    
@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    user = User.query.get_or_404(username)
    feedbacks = user.feedbacks    
    if user.username == session['username'] and 'username' in session:
        
        if feedbacks:
            for feedback in feedbacks:
                db.session.delete(feedback)
            db.session.delete(user)
            db.session.commit()
            session.pop('username')
            return redirect('/')
        else:
            db.session.delete(user)
            db.session.commit()
            session.pop('username') 
        
        return redirect('/')
    flash("can't delete other users", 'danger')
    return redirect(f'/users/{user.username}')

@app.route('/users/<username>/feedback/add', methods=['GET','POST'])
def feedback_form(username):
    form = FeedbackForm()
    
    if username == session['username']:
    
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            
            new_feed = Feedback.new_feed(title = title, content = content, username=username)
            db.session.add(new_feed)
            db.session.commit()
            flash('Successfully added new feedback', 'success')
            return redirect(f'/users/{username}')
        
        
        return render_template('feedback_form.html',form=form)
    
    flash("can't access other users pages")
    current_user = session['username']
    return redirect(f'/users/{current_user}')

@app.route('/feedback/<feedback_id>/update', methods=['GET', 'POST'])
def update_feed(feedback_id):
    feedback = Feedback.query.filter_by(id=feedback_id).first()
    user = feedback.user
    form = FeedbackForm(obj = feedback)
    
    if feedback.user.username == session['username']:
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data

            feedback.update_feed(title=title, content=content)
            flash('success edit', 'info')
            return redirect(f'/users/{user.username}')
        return render_template('feedback_form.html', form=form)
    
    curr_user = session['username']
    flash('can not edit others feeds', 'danger')
    return redirect(f'/users/{curr_user}')

@app.route('/feedback/<feedback_id>/delete', methods=['POST'])
def deleteFeedback(feedback_id):
    """Delete a feedback"""
    feedback = Feedback.query.get(feedback_id)
    if 'username' not in session or feedback.user.username != session['username']:
        flash('please login first', 'danger')
        return redirect('/login')
    if feedback.user.username == session['username']:
        db.session.delete(feedback)
        db.session.commit()
        
        flash('Deleted feedback', 'danger')
        return redirect(f'/users/{feedback.user.username}')  
    
    curr_user = session['user']
    
    flash("can not delete other users' feedback", 'danger')
    return redirect(f'/users/{curr_user}')  
    
@app.route('/register', methods=['GET', 'POST'])
def register_form():
    """Page with registration form"""
    form = UserRegistrationForm()
    
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        
        new_user = User.register(username=username, pwd = password, email=email, first_name = first_name, last_name=last_name)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username already exists')
            return render_template('register.html', form=form)
            
        session['username'] = new_user.username
        flash('Successfully registered', 'success')
        
        return redirect(f'/users/{new_user.username}')
    
    return render_template('register.html',form = form)

@app.route('/login', methods=['GET','POST'])
def login_form():
    form = UserLoginForm()
    
    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data
        
        user = User.authentication(username, pwd)
        
        if user:
            flash(f'welcome back, {user.username}', 'info')
            session['username'] = user.username
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors = ['incorrect username or password']
        
        
    return render_template('login.html',form = form)

@app.route('/logout', methods = ['POST'])
def logout_user():
    session.pop('username')
    flash('logged out')
    
    return redirect('/')