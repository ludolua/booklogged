from flask import Flask, render_template, request, redirect, url_for
import requests
import sqlite3

app = Flask(__name__)


def init_db():
    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS books
                 (id INTEGER PRIMARY KEY, title TEXT, authors TEXT, description TEXT)''')
    conn.commit()
    conn.close()

init_db()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        search_query = request.form['search']
        books = search_books(search_query)
        return render_template('index.html', books=books)
    return render_template('index.html')


def search_books(query):
    response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={query}')
    return response.json().get('items', [])


@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form['title']
    authors = request.form['authors']
    description = request.form['description']

    conn = sqlite3.connect('books.db')
    c = conn.cursor()
    c.execute("INSERT INTO books (title, authors, description) VALUES (?, ?, ?)", 
              (title, authors, description))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
