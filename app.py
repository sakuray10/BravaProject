from flask import Flask, render_template, request, url_for, flash, redirect
from init_db import init_db
import sqlite3
from werkzeug.exceptions import abort

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bravaproject'

init_db()


# establish database connection, returns rows as python dicts
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# display a blog post
def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/community')
def community():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('community.html', posts=posts)


@app.route('/new', methods=('GET', 'POST'))
def new():
    if request.method == 'POST':
        option = request.form['option']
        email = request.form['email']
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required.')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (option, email, title, content) VALUES (?, ?, ?, ?)',
                         (option, email, title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('community'))

    return render_template('newpostform.html')


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


if __name__ == '__main__':
    app.run()
