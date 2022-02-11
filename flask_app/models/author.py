from flask_app.config.mysqlconnection import connectToMySQL

from flask_app.models import book, author

class Author:
  def __init__(self, db_data):
    self.id = db_data['id']
    self.name = db_data['name']
    self.created_at = db_data['created_at']
    self.updated_at = db_data['updated_at']
    self.favorites = []
  
  #Create

  @classmethod
  def save(cls, data):
    query = "INSERT INTO authors ( name , created_at , updated_at ) VALUES (%(name)s,NOW(),NOW());"
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    return connectToMySQL('books_schema').query_db(query,data)

  #Read

  @classmethod
  def get_all(cls):
    query = "SELECT * FROM authors;"
    books_from_db = connectToMySQL('books_schema').query_db(query)
    books = []
    for b in books_from_db:
      books.append(cls(b))
    return books

  @classmethod
  def get_one_with_favorites(cls, data):
    query = """
    SELECT * 
    FROM books_schema.authors 
    JOIN books_schema.favorites ON books_schema.authors.id = books_schema.favorites.author_id 
    JOIN books_schema.books ON books_schema.books.id = books_schema.favorites.book_id 
    WHERE books_schema.authors.id = %(id)s
    ;"""
    data = connectToMySQL('books_schema').query_db(query,data)
    author = cls(data[0])
    for row in data: # think of this "row" as each row in a table
      if row['books.id'] == None:
        break
      else:
        data = {
          'id' : row['books.id'],
          'title' : row['title'],
          'num_of_pages' : row['num_of_pages'],
          'created_at' : row['books.created_at'],
          'updated_at' : row['books.updated_at'],
        }
        every_book_in_author = book.Book(data)
        author.favorites.append(every_book_in_author)
    return author
    
  @classmethod
  def unfavorited_authors(cls,data):
    query = "SELECT * FROM authors WHERE authors.id NOT IN ( SELECT author_id FROM favorites WHERE book_id = %(id)s );"
    authors = []
    results = connectToMySQL('books_schema').query_db(query,data)
    for row in results:
      authors.append(cls(row))
    return authors

  #Update


  #Delete