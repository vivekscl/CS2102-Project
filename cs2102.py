import os
from app import create_app, ItemForm, LoginForm, SignUpForm, login_manager
from flask_login import login_required, logout_user, login_user, current_user
from models import user as user_model, listing as listing_model, bid as bid_model, loan as loan_model
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


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', current_time=datetime.utcnow())


@app.route('/user', methods=['GET'])
@login_required
def user_page():
    listings = listing_model.get_listings_under_owner(current_user.id)
    loans = loan_model.get_loans_under_bidder(current_user.id)
    available = []
    not_available = []

    print(loans)
    for listing in listings:
        if listing.is_available == 'true':
            available.append(listing)
        else:
            not_available.append(listing)

    return render_template('user.html', available=available, not_available=not_available, loans=loans)

@app.route('/listing/create', methods=['GET', 'POST'])
@login_required
def create_listing():

    form = ItemForm()

    # If a post request is sent, validate the form and insert the listing into the db using listing_model
    if request.method == 'POST':
        if form.validate_on_submit():
            listing = listing_model.Listing(None, current_user.id, form.item_name.data, form.description.data)
            if listing.create_listing():
                flash("New listing added!", "success")
                return redirect(url_for('index'))
            else:
                flash('Unable to add the listing!', "error")
                app.logger.warning("Insert failed") # to-do provide error msg for diff insertion error


    return render_template('create_listing.html', form=form, current_time=datetime.utcnow())

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
