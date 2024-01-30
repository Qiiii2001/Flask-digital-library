from flask import Blueprint, render_template, flash
from models import db, Book, book_schema
from forms import BookForm
from flask import request, jsonify, redirect, url_for

site = Blueprint('site',__name__,template_folder='site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
def profile():
    return render_template('profile.html')

@site.route('/contact')
def contact():
    return render_template('contact.html')



# Create Book
@site.route('/book', methods=['POST'])
def create_book():
    form = BookForm(request.form)
    if form.validate_on_submit():
        new_book = Book (
            title = form.title.data,
            author=form.author.data,
            isbn=form.isbn.data,
            length=form.length.data, 
            format=form.format.data 
        )
        db.session.add(new_book)
        db.session.commit()
        
        # Json Response
        # return book_schema.jsonify(new_book)
        return redirect(url_for('site.get_books'))



@site.route('/books',methods=['GET'])
def get_books():
    books = Book.query.all()
    # Json Response
    # book_schema = BookSchema(many=True) 
    # return jsonify(book_schema.dump(books))
    return render_template('book_list.html', books=books)
    


# add_book form
@site.route('/add_book', methods=['GET', 'POST'])
def add_book():
    form = BookForm()
    if form.validate_on_submit():
        new_book = Book(title=form.title.data, author=form.author.data, isbn=form.isbn.data,length=form.length.data,format=form.format.data)
        db.session.add(new_book)
        db.session.commit()
        # Json Response
        # book_data = book_schema.dump(new_book)
        # return jsonify(book_data), 201 
        return redirect(url_for('site.get_books'))
    return render_template('book_form.html', form=form)



    
@site.route('/book/<string:id>', methods=['GET'])
def get_book(id):
    book = Book.query.get_or_404(id)
    return render_template('book_detail.html',book=book)
   


# Update Book
@site.route('/update_book/<string:id>', methods=['GET', 'POST'])
def update_book(id):
    book = Book.query.get_or_404(id)
    form = BookForm(obj=book) 

    if form.validate_on_submit():  
        book.title = form.title.data
        book.author = form.author.data
        book.isbn = form.isbn.data
        book.length = form.length.data
        book.format = form.format.data
        db.session.commit()
        flash('Book updated successfully!', 'success')
        # Api
        # return jsonify(book_data), 200
        return redirect(url_for('site.get_books'))
    
    return render_template('book_form.html', form=form, book=book)  # Moved outside of the POST request check


@site.route('/delete_book/<string:id>',methods=['POST'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    flash('Book deleted successfully!', 'success')
    # Api
    # return jsonify(response), 200
    return redirect(url_for('site.get_books'))

@site.route('/search')
def search():
    query = request.args.get('query')
    if query:
        # Search by 'make' and 'model' fields 
        results = Book.query.filter(
            (Book.title.ilike('%' + query + '%')) | 
            (Book.author.ilike('%' + query + '%')) |
            (Book.isbn.cast(db.String).ilike('%' + query + '%'))
        ).all()
    else:
        results = []
    # Json Response
    # return jsonify({'query': query, 'results': result_data})
    return render_template('search_results.html', query=query, results=results)

@site.route('/contact_submit', methods=['POST'])
def contact_submit():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    
    flash('Thank you for your message, we will get back to you shortly.')
    
    return redirect(url_for('site.home'))