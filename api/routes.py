from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import DVD
from . import db
from flask_login import login_user, login_required, logout_user, current_user

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

@dvd.route('/remove-dvd/<int:id>', methods=['GET', 'POST'])
def remove_dvd(id):
    dvd = DVD.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(dvd)
        db.session.commit()
        flash('DVD removed successfully!', category='success')
        return redirect(url_for('dvd.view_dvds'))
    return render_template('confirm_remove.html', dvd=dvd)

@dvd.route('/edit-dvd/<int:id>', methods=['GET', 'POST'])
def edit_dvd(id):
    dvd = DVD.query.get_or_404(id)
    if request.method == 'POST':
        dvd.title = request.form.get('title')
        dvd.category = request.form.get('category')
        dvd.running_time = request.form.get('running_time')
        dvd.year = request.form.get('year')
        dvd.price = request.form.get('price')
        db.session.commit()
        flash('DVD updated successfully!', category='success')
        return redirect(url_for('dvd.view_dvds'))
    return render_template("edit_dvd.html",user=current_user, dvd=dvd)

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

# @dvd.route('/view-by-category', methods=['GET', 'POST'])
# def view_by_category():
#     if request.method == 'POST':
#         category = request.form.get('category')
#         dvds = DVD.query.filter_by(category=category).all()
#         return render_template("view_by_category.html", user=current_user, dvds=dvds)
#     return render_template("view_by_category.html", user=current_user)


@dvd.route('/view-by-year')
def view_by_year():
    dvds = DVD.query.order_by(DVD.year).all()
    return render_template("view_by_year.html",user=current_user, dvds=dvds)
