from flask import render_template,redirect,request,session,flash  

from flask_app import app

from flask_app.models import author

# CREATE

@app.route('/create/author', methods=['POST'])
def create_author():
  print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
  data = {
    "name":request.form['name'],
  }
  author.Author.save(data)
  # dojo_id = request.form['dojo_id']
  return redirect('/authors')

# READ

@app.route('/')
def index():
  return render_template("author.html")

@app.route('/authors')
def authors_get_all():
  author_list = author.Author.get_all()
  return render_template("author.html", authors=author_list)

@app.route('/authors/<int:id>')
def get_one_author(id):
  data = {
    'id' : id
  }
  this_author = author.Author.get_one_with_favorites(data)
  return render_template('show_authors.html', author=this_author)

# @app.route('authors.')

#   return redirect(f/blah/{author.id})
