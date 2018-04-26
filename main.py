from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'secretkey'

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(255))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return self.username

@app.before_request
def require_login():
    allowed_routes = ['login', 'register','blog','index']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/')
def index():
    users = User.query.all()
    return render_template('index.html', users=users)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            flash("Logged in")
            return render_template('newpost.html')
        else:
        
            flash('User password incorrect, or user does not exist')

    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']

        existing_user = User.query.filter_by(username=username).first()
        if password == verify:

            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                return redirect('/')
            else:
         
                return "<h1>Duplicate user</h1>"
        else:
            flash('passwords must match') 
            return render_template('signup.html')
    return render_template('signup.html')

@app.route('/blog', methods=['POST','GET'])
def blog():
    posts = Blog.query.all()
    users = User.query.all()
    post_id = request.args.get('id')
    user_id = request.args.get('user')
    onepost = Blog.query.filter_by(id=post_id).all()
    user = Blog.query.filter_by(owner_id=user_id).all()
    author = User.query.filter_by(id=user_id).all()

    if post_id:
        return render_template('blogpage.html', posts=onepost, author=author)
    elif user_id:
        return render_template('singleuser.html', posts=user, author=author)
    else:
        return render_template('blogpage.html', posts=posts, users=users, author=author)

@app.route('/newpost', methods=['GET','POST'])
def newpost():

    if request.method=='POST':
        title = request.form['title']
        body = request.form['body']
        title_error = ''
        body_error = ''
        owner_id = User.query.filter_by(username=session['username']).first()
        new_post = Blog(title, body, owner_id)

        if title == '':
            title_error = 'please enter a title'
        
        if body == '':
            body_error = 'please enter a body'

        if body_error =='':
            if title_error =='':
            
                db.session.add(new_post)
                db.session.commit()
                post_id = str(new_post.id)
                #user_id = str(new_post.owner_id)
 
                return redirect('/blog?id='+post_id)

        return render_template('newpost.html', title=title, title_error=title_error, body=body, body_error=body_error)

    return render_template('newpost.html')


@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')

if __name__ == '__main__':
    app.run()