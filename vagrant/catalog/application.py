from flask import Flask, render_template, request, redirect, jsonify, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Genre, Movie

app = Flask(__name__)

engine = create_engine('sqlite:///catalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# JSON endpoints
@app.route('/movie/JSON')
def moviesJSON():
    movies = session.query(Movie).all()
    return jsonify(movies=[m.serialize for m in movies])


# Show all genres
@app.route('/')
@app.route('/genre/')
def showGenres():
    genres = session.query(Genre).all()
    return render_template('genres.html', genres=genres)


# Create a new genre
@app.route('/genre/new/', methods=['GET', 'POST'])
def newGenre():
    if request.method == 'POST':
        newGenre = Genre(name=request.form['name'])
        session.add(newGenre)
        session.commit()
        return redirect(url_for('showGenres'))
    else:
        return render_template('newGenre.html')


# Edit a genre
@app.route('/genre/<int:genre_id>/edit/', methods=['GET', 'POST'])
def editGenre(genre_id):
    editedGenre = session.query(
        Genre).filter_by(id=genre_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedGenre.name = request.form['name']
            return redirect(url_for('showGenres'))
    else:
        return render_template(
            'editGenre.html', genre=editedGenre)

    # return 'This page will be for editing genre %s' % genre_id

# Delete a genre


@app.route('/genre/<int:genre_id>/delete/', methods=['GET', 'POST'])
def deleteGenre(genre_id):
    genreToDelete = session.query(
        Genre).filter_by(id=genre_id).one()
    if request.method == 'POST':
        session.delete(genreToDelete)
        session.commit()
        return redirect(
            url_for('showGenres', genre_id=genre_id))
    else:
        return render_template(
            'deleteGenre.html', genre=genreToDelete)
    # return 'This page will be for deleting genre %s' % genre_id


# Show a genre menu
@app.route('/genre/<int:genre_id>/')
@app.route('/genre/<int:genre_id>/menu/')
def showMenu(genre_id):
    genre = session.query(Genre).filter_by(id=genre_id).one()
    items = session.query(Movie).filter_by(
        genre_id=genre_id).all()
    return render_template('menu.html', items=items, genre=genre)
    # return 'This page is the menu for genre %s' % genre_id

# Create a new menu item


@app.route(
    '/genre/<int:genre_id>/menu/new/', methods=['GET', 'POST'])
def newMovie(genre_id):
    if request.method == 'POST':
        newItem = Movie(name=request.form['name'], description=request.form[
                           'description'], price=request.form['price'], course=request.form['course'], genre_id=genre_id)
        session.add(newItem)
        session.commit()

        return redirect(url_for('showMenu', genre_id=genre_id))
    else:
        return render_template('newmenuitem.html', genre_id=genre_id)

    return render_template('newMovie.html', genre=genre)
    # return 'This page is for making a new menu item for genre %s'
    # %genre_id

# Edit a menu item


@app.route('/genre/<int:genre_id>/menu/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def editMovie(genre_id, menu_id):
    editedItem = session.query(Movie).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['name']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['course']:
            editedItem.course = request.form['course']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('showMenu', genre_id=genre_id))
    else:

        return render_template(
            'editmenuitem.html', genre_id=genre_id, menu_id=menu_id, item=editedItem)

    # return 'This page is for editing menu item %s' % menu_id

# Delete a menu item


@app.route('/genre/<int:genre_id>/menu/<int:menu_id>/delete',
           methods=['GET', 'POST'])
def deleteMovie(genre_id, menu_id):
    itemToDelete = session.query(Movie).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        return redirect(url_for('showMenu', genre_id=genre_id))
    else:
        return render_template('deleteMovie.html', item=itemToDelete)
    # return "This page is for deleting menu item %s" % menu_id


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
