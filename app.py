# Importing flask module in the project is mandatory
#Render template is used to load in HTML files
from flask import Flask, render_template, request, redirect, url_for, flash
import random
import sqlite3
# We use this to set up our flask sever
app = Flask(__name__)

@app.route('/')
# ‘/’ URL is bound with index() function.
def index():
    return render_template("index.html")

def get_db_connection():
    conn = sqlite3.connect('games.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    with app.open_resource('schema.sql') as f:
        conn.executescript(f.read().decode('utf8'))
    conn.close()

@app.route('/new',methods=('POST','GET'))
def New_games():
    if request.method == 'POST':
        game_name = request.form['game_name']
        platform = request.form['platform']
        genre = request.form['genre']
        year = request.form['year']
        sales = request.form['sales']

        if not game_name or not platform:
            flash('All fields required')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO games (title,platform,genre,year,sales) VALUES (?,?,?,?,?)',(game_name,platform,genre,year,sales))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template("login.html")

@app.route('/admin')
def admin():
    conn = get_db_connection()
    sql = "SELECT * FROM games"
    game = conn.execute(sql).fetchall()
    conn.close()
    #print(user)
    return render_template('view_users.html',game=game)

# Route to edit a game
@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit_user(id):
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM games WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        user_name = request.form['userName']
        password = request.form['password']

        if not user_name or not password:
            flash('All fields are required!')
        else:
            conn.execute('UPDATE users SET username = ?, password = ? WHERE id = ?',
                         (user_name, password,id))
            conn.commit()
            conn.close()
            return redirect(url_for('admin'))

    return render_template('edit_user.html', users=users)


# Route to delete a game
@app.route('/delete/<int:id>', methods=('POST',))
def delete_user(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM users WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('User deleted successfully!')
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True, port=7654)