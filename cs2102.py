import os
from app import create_app, LoginForm, SignUpForm, login_manager, SearchForm, SearchByOwnerForm
from flask_login import login_required, logout_user, login_user
from models import user as user_model, listing as listing_model, bid as bid_model, tag as tag_model, listing_tag as listing_tag_model
from werkzeug.security import generate_password_hash
from flask import render_template, redirect, url_for, g, flash, request
from datetime import datetime

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@login_manager.user_loader
def load_user(user_id):
    """
    This method is called automatically by Flask-Login to get the user by his id whenever Flask-Login needs the User
    object.
    :param user_id:
    :return: User who's id his the given id
    """
    return user_model.get_user_by_id(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    This route contains the login page and the login form. When submitted, we verify if the user exists in the database
    and his credentials are correct.
    :return:
    """
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = user_model.get_user_by_username(form.username.data)

        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            # If the user wanted to access from a different page instead of the home page, we can keep track of
            # of this url so as to redirect the user back
            next_url = request.args.get('next')
            if next_url is None or not next_url.startswith('/'):  # check that the next_url is a relative URL
                next_url = url_for('index')
            return redirect(next_url)
        flash("Invalid username or password", "error")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    """
    Use the Flask-Login's implementation of logout user.
    :return:
    """
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    This route contains the sign up page and form. When submitted, we create the user in the database and redirect them
    to the login page for them to login immediately.
    :return:
    """
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = user_model.User(None, form.username.data, form.name.data,
                               generate_password_hash(form.password.data), form.phonenumber.data)
        user.create_user()
        flash("You can now login", "success")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = SearchForm();
    form2 = SearchByOwnerForm();
    if form.validate_on_submit():
        return redirect(url_for('search_results', query=form.search.data))
    if form2.validate_on_submit():
        return redirect(url_for('search_results_owner', query=form2.search.data))
    return render_template('index.html', form=form, form2=form2, current_time=datetime.utcnow())


@app.route('/user', methods=['GET'])
@login_required
def user_page():
    return render_template('user.html', current_time=datetime.utcnow())


@app.route('/search_results/<query>', methods=['GET'])
def search_results(query):
    if not query:
        listing = listing_model.get_all_listing()
    else:
        listing = listing_model.get_listings_by_tag_name(query)
    return render_template('search_results.html', listing=listing)


@app.route('/search_results_owner/<query>', methods=['GET'])
def search_results_owner(query):
    if not query:
        listing = listing_model.get_all_listing()
    else:
        listing = listing_model.get_listings_by_owner_name(query)
    return render_template('search_results_owner.html', listing=listing)



@app.route('/listing/<int:listing_id>', methods=['GET'])
def listing_details(listing_id):
    """
    The route shows the listing details of the given listing ID
    :param listing_id:
    """
    listing = listing_model.get_listing_by_id(listing_id)
    bids = bid_model.get_bids_under_listing(listing_id)
    owner = user_model.get_user_by_id(listing.owner_id)
    return render_template('listing.html', listing=listing, bids_under_this_listing=bids, owner=owner)
