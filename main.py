from flask import Flask, request, redirect, render_template, url_for, session
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Blogz:root@localhost:8889/Blogz'

app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    blog_title= db.Column(db.String(120))
    blog_post = db.Column(db.Text)
    owner_id = db.column(db.Integer,db.ForeignKey('user.id'))
  
    def __init__(self, blog_title, blog_post, owner):
        self.blog_title = blog_title
        self.blog_post = blog_post
        self.owner = owner
        
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(150))
    password = db.Column(db.String(50))
    blogs = db.relationship('Blog',backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ['login','blog','index','signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect(url_for('login'))


@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'] 
        verify_password = request.form['verify']
        email = request.form['email']

        username_error_msg =""
        password_error_msg =""
        verify_password_error_msg =""
        email_error_msg =""

        if len(username) < 3 or len(username) > 20 or " " in username:
            username_error_msg = "Invalid username"
            username = ""
        if len(password) < 3 or len(password) > 20 or " " in password:
            password_error_msg = "Invalid Password"
            password = "" 
        if password != verify_password or verify_password =="":
            verify_password_error_msg = "Password does not match"
            verify_password = ""
        if email != "" and len(email) < 3 or len(email) > 20:
            email_error_msg = "Incorrect email"
            email= ""

        elif email != "" and (" " not in email or "@" not in email or "." not in email):
            email_error_msg = "Incorrect email"
            email = ""

        if not username_error_msg and not password_error_msg and not verify_password_error_msg and not email_error_msg:
            existing_user =User.query.filter_by(username = username).first()
            if not existing_user:
                new_user = User(username, password)
                db.session.add(new_user)
                db.session.commit()
                session['username'] = username
                   return redirect(url_for('newpost'))
            else:
                flash('User Already Exist', "error_message")
        else:
            return render_template('signup.html', username_error_msg = username_error_msg, password_error_msg = password_error_msg,verify_password_error_msg = verify_password_error_msg,email_error_msg = email_error_msg, username = username, email =email)
    return render_template('signup.html')


@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username = username).first()

        if user is None:
            flash('User does not exist','Error_message')
            return redirect(url_for('login'))
        else:
            if user.password == password:
                session ['username'] = username
                return redirect(url_for('newpost'))
            elif user.password != password:
                flash('Incorrect Password')
                return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout')
def logout():
    del session['username']
    return redirect(url_for('blog'))
    
@app.route('/', methods=('POST','GET'))
def index():
    users = User.query.all()
    return render_template('index.html', users = users)

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    owners = User.query.all()
    blog_posts = Blog.query.all()
    users_blog_entries = []

    if "id" in request.args:
        blog_id = request.args.get('id')
        blog_entry = Blog.query.get(blog_id)
        return render_template("single-post.html", blog_title = blog_content.blog_title, blog_content = blog_content.blog_post, username = blog_entry.owner.username)
    elif "user" in request.args:
        blog_user = request.args.get("user")
        for owner in owners:
            if owner.username == blog_user:
                users_blog_entries = Blog.query.filter_by(owner = owner).all()
        return render_template("singleUser.html", user_entries = users_blog_entries)
    else:
        return render_template("blogz.html", title = "BLOG POSTS!", blogposts = blog_posts)

@app.route('/newpost', methods = ['POST','GET'])
def newpost():
    owner = user.query.filter_by(username=session['username']).first()
    if request.method == "POST":
        blog_title_error = ""
        blog_body_error = ""
        blog_title_content = ""
        blog_post_content = ""

        if request.form["blog_title"] == "" or request.form["blog_post"]== "":
            if request.form["blog_title"] =="":
                blog_title_error = "Please give a title to your blog"
            else:
                blog_title_content =request.form["blog_title"]
    
            if request.form["blog_post"] =="":
                blog_body_error = "Please type in a body to your post"
            else:
                blog_post_content = request.form["blog_post"]

        if blog_title_error or blog_body_error:
            return render_template("newpost.html",blog_title_content = blog_title_content,blog_post_content = blog_post_content,blog_title_error = blog_title_error,blog_body_error = blog_body_error)
        else:
            blogtitle = request.form["blog_title"]
            newpost = request.form["blog_post"]
            new_blog = Blog(blogtitle,newpost)
            db.session.add(new_blog)
            db.session.commit()
            return redirect(url_for("blog", id = [new_blog.id]))
    return render_template('newpost.html')


if __name__ == '__main__':
    app.run()