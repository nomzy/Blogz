from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:root@localhost:8889/build-a-blog'

app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    blog_title= db.Column(db.String(120))
    blog_post = db.Column(db.Text)
    
    
    def __init__(self, blog_title, blog_post):
        self.blog_title = blog_title
        self.blog_post = blog_post
        
db.create_all()
db.session.commit()

@app.route('/', methods=('POST','GET'))
def index():
    return render_template('newpost.html')

@app.route('/blog', methods=['POST', 'GET'])
def blog():
    blog_posts = Blog.query.all()
    blog_id = request.args.get('id')
    if blog_id is None:
        return render_template("blog.html", title="BUILD A BLOG", blogposts = blog_posts)
    else:
        blog_content = Blog.query.get(blog_id)
        return render_template("single-post.html", blog_title = blog_content.blog_title, blog_content = blog_content.blog_post)
    return render_template('blog.html')

@app.route('/newpost', methods = ['POST','GET'])
def newpost():
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