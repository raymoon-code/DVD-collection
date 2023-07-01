from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import DVD,Product,Post
from . import db
from flask_login import login_user, login_required, logout_user, current_user
import traceback
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

DB_NAME = 'database.db'
app.config['SECRET_KEY'] = 'RAYMOON'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

dvd = Blueprint('dvd', __name__)

@dvd.route('/add-dvd', methods=['GET', 'POST'])
def add_dvd():
    if request.method == 'POST':
        title = request.form.get('title')
        category = request.form.get('category')
        running_time = request.form.get('running_time')
        year = request.form.get('year')
        price = request.form.get('price')
        new_dvd = DVD(title=title, category=category, running_time=running_time, year=year, price=price)
        db.session.add(new_dvd)
        db.session.commit()
        flash('DVD added successfully!', category='success')
        # return redirect(url_for('dvd.view_dvds'))
    return render_template("add_dvd.html",user=current_user)

@dvd.route('/add-product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        title = request.form['title']
        price = float(request.form['price'])
        description = request.form['description']
        image_url = request.form['image_url']
        amazon_link = request.form['amazon_link']

        new_product = Product(title=title, price=price, description=description, image_url=image_url, amazon_link=amazon_link)
        db.session.add(new_product)
        db.session.commit()
        flash('Product added to the database!', category='success')
        
    return render_template('add_product.html',user=current_user)

@dvd.route('/remove-dvd/<int:id>', methods=['GET', 'POST'])
def remove_dvd(id):
    try:
        dvd = DVD.query.get_or_404(id)
        if request.method == 'POST':
            db.session.delete(dvd)
            db.session.commit()
            flash('DVD removed successfully!', category='success')
            return redirect(url_for('dvd.view_dvds'))
        return render_template('confirm_remove.html', dvd=dvd)
    except Exception as e:
        error_message = traceback.format_exc()
        return render_template('error.html', error=error_message)

@dvd.route('/edit-dvd/<int:id>', methods=['GET', 'POST'])
def edit_dvd(id):
    try:
        dvd = DVD.query.get_or_404(id)
        if request.method == 'POST':
            dvd.title = request.form.get('title')
            dvd.category = request.form.get('category')
            dvd.running_time = request.form.get('running_time')
            dvd.year = request.form.get('year')
            dvd.price = request.form.get('price')
            with app.app_context():
                # dvd = DVD.query.get_or_404(id)
                # dvd.title = request.form.get('title')
                db.session.commit()
            db.session.commit()
            flash('DVD updated successfully!', category='success')
            return redirect(url_for('dvd.view_dvds'))
        return render_template("edit_dvd.html",user=current_user, dvd=dvd)
    except Exception as e:
        error_message = traceback.format_exc()
        return render_template('error.html', error=error_message)

@dvd.route('/view-products')
def view_products():
    products = Product.query.all()
    return render_template('products.html',user=current_user, products=products)

@dvd.route('/top-10')
def top_10():
    products = Product.query.all()
    return render_template('top10.html',user=current_user, products=products)


@dvd.route('/view-dvds', methods=['GET', 'POST'])
def view_dvds():
    categories = set([dvd.category for dvd in DVD.query.all()])
    dvds = DVD.query.all()
    selected_category = None

    if request.method == 'POST':
        selected_category = request.form.get('category')
        if selected_category == None:
            dvds = DVD.query.all()
        else:
            dvds = DVD.query.filter_by(category=selected_category).all()
        if request.method == 'POST' and 'sort_by_year' in request.form:
            dvds = DVD.query.order_by(DVD.year).all()
    return render_template("view_dvds.html", user=current_user, dvds=dvds, categories=categories, selected_category=selected_category)

@dvd.route('/view-by-category/<string:category>')
def view_by_category(category):
    dvds = DVD.query.filter_by(category=category).all()
    return render_template("view_by_category.html",user=current_user, dvds=dvds)

@dvd.route('/create-post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        opening = request.form['opening']
        product_ids = request.form.getlist('product')
        conclusion = request.form['conclusion']
        
        post = Post(title=title, opening=opening, product_ids=','.join(product_ids), conclusion=conclusion)
        db.session.add(post)
        db.session.commit()
        flash('post created successfully!', category='success')
        # return render_template('view_posts.html',user=current_user, post=post)
    
    products = Product.query.all()
    return render_template('create_post.html',user=current_user, products=products)

@dvd.route('/posts')
def view_posts():
    posts = Post.query.all()
    products = Product.query.all()
    return render_template('view_posts.html',user=current_user, posts=posts,products=products)

@dvd.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    products = Product.query.all()

    if request.method == 'POST':
        post.title = request.form['title']
        post.opening = request.form['opening']
        post.product_ids = ','.join(request.form.getlist('product'))
        post.conclusion = request.form['conclusion']
        
        db.session.commit()
        flash('Post updated successfully!', category='success')
        return redirect(url_for('dvd.view_posts'))

    return render_template('edit_post.html', user=current_user, post=post, products=products)


@dvd.route('/delete-post/<int:post_id>', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted successfully!', category='success')
    return redirect(url_for('dvd.view_posts'))
    # return render_template('confirm_remove.html', dvd=dvd, user=current_user)


@dvd.route('/view-by-year')
def view_by_year():
    dvds = DVD.query.order_by(DVD.year).all()
    return render_template("view_by_year.html",user=current_user, dvds=dvds)
