from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(255))

    def __init__(self, title, body):
        self.title = title
        self.body = body


@app.route('/')
def index():
    return render_template('blogpage.html')

@app.route('/blog')
def blog():
    
    return render_template('blogpage.html')

@app.route('/newpost', methods=['GET','POST'])
def newpost():

    if request.method=='POST':
        title = request.form['title']
        body = request.form['body']
        title_error = ''
        body_error = ''
        new_post=Blog(title, body)

        if title == '':
            title_error = 'please enter a title'
        
        if body == '':
            body_error = 'please enter a body'

        if body_error =='':
            if title_error =='':
            
                db.session.add(new_post)
                db.session.commit()
                post = Blog.query.all()
                return render_template('blogpage.html', post=post)

        return render_template('newpost.html', title=title, title_error=title_error, body=body, body_error=body_error)

    return render_template('newpost.html')

if __name__ == '__main__':
    app.run()