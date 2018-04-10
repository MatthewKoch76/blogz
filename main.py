from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:password@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

@app.route('/', methods=['POST', 'GET'])
def index():

    return render_template('blogpage.html')

@app.route('/addpost', methods=['POST', 'GET'])
def addpost():

    return render_template('addpost.html')


if __name__ == '__main__':
    app.run()