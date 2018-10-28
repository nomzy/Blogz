from flask import Flask, request, redirect, render_template 
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URL'] = 'mysql+pymysql://Build-a-Blog:root@localhost:8889/Build-a-Blog'

app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    blog_post = db.Column(db.Text)
    blog_title= db.Column(db.String(120))
    
    def __init__(self, blog_title, blog_post):
        self.blog_post = blog_post
        self.blog_title = blog_title
        

@app.route('/')
def index():
    return render_template('newpost.html')

# @app.route('/blog', methods=['POST', 'GET'])
# def index():
#     if request.method == 'POST':
#         Blog = request.form['Blog']
#         Blog.append(Blog)
#     return render_template('index.html', title="Build-a-Blog", Blog=Blog)

# @app.route('/newpost')
# def index():
#     return render_template('index.html', title="Build-a-Blog", newpost=newpost)


if __name__ == '__main__':
    app.run()