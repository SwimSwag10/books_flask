from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models import author

class Book:
  def __init__(self, db_data):
    self.id = db_data['id']
    self.title = db_data['title']
    self.num_of_pages = db_data['num_of_pages']
    self.created_at = db_data['created_at']
    self.updated_at = db_data['updated_at']
    self.favorites = []
  
  #Create

  @classmethod
  def save(cls, data):
    query = "INSERT INTO books ( title , num_of_pages , created_at , updated_at ) VALUES (%(title)s,%(num_of_pages)s,NOW(),NOW());"
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    return connectToMySQL('books_schema').query_db(query,data)

  #Read

  @classmethod
  def get_all(cls):
    query = "SELECT * FROM books;"
    books_from_db = connectToMySQL('books_schema').query_db(query)
    books = []
    for row in books_from_db:
      books.append(cls(row))
    return books

  @classmethod
  def get_one_with_favorites(cls, data):
    query = """
    SELECT * 
    FROM books_schema.books
    JOIN books_schema.favorites ON books_schema.books.id = books_schema.favorites.book_id 
    JOIN books_schema.authors ON books_schema.authors.id = books_schema.favorites.author_id 
    WHERE books_schema.books.id = %(id)s
    ;"""
    results = connectToMySQL('books_schema').query_db(query,data)
    book = cls(results[0])
    for row in results: # think of this "row" as each row in a table
      if row['authors.id'] == None:
        break
      else:
        data = {
          'id' : row['authors.id'],
          'name' : row['name'],
          'created_at' : row['authors.created_at'],
          'updated_at' : row['authors.updated_at'],
        }
        every_author_in_book = author.Author(data)
        book.favorites.append(every_author_in_book)
    return book

  #Update

  @classmethod
  def unfavorited_books(cls,data):
    query = "SELECT * FROM books WHERE books.id NOT IN ( SELECT book_id FROM favorites WHERE author_id = %(id)s );"
    results = connectToMySQL('books_schema').query_db(query,data)
    books = []
    print("why is this not working I'm not sure whty this is not working!!!!!!!!!!!!!!!")
    for row in results:
      books.append(cls(row))
    print(books)
    return books

  #Delete