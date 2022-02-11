from flask import render_template,redirect,request,session,flash  

from flask_app import app

from flask_app.models import book, author

# CREATE

@app.route('/create/book', methods=['POST', 'GET'])
def create_book():
  data = {
    "title" : request.form['title'],
    "num_of_pages" : request.form['num_of_pages']
  }
  book.Book.save(data)
  return redirect('/books')

#READ

@app.route('/books')
def books_get_all():
  books = book.Book.get_all()
  return render_template('book.html', all_books=books)

@app.route('/books/<int:id>')
def books_show(id):
  data = {
    "id" : id
  }
  book_list = book.Book.get_one_with_favorites(data)
  unfavorited_authors = author.Author.unfavorited_authors(data)
  return render_template("show_books.html", books=book_list, unfavorited_authors=unfavorited_authors)

# UPDATE

@app.route('/join/author',methods=['POST'])
def join_author():
    data = {
        'author_id': request.form['author_id'],
        'book_id': request.form['book_id']
    }
    author.Author.get_one_with_favorites(data)
    return redirect(f"/book/{request.form['book_id']}")