import os
from app import create_app, ItemForm, LoginForm, SignUpForm, login_manager
from app import create_app, ItemForm, LoginForm, SignUpForm, BidForm, GenerateLoanForm, login_manager
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


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.template_filter('convert_bidder_id_to_name')
def convert_bidder_id_to_name(bidder_id):
    return user_model.get_user_by_id(bidder_id).name


@app.template_filter('convert_listing_id_to_name')
def convert_listing_id_to_name(listing_id):
    return listing_model.get_listing_by_id(listing_id).name


@app.template_filter('convert_listing_id_to_description')
def convert_listing_id_to_description(listing_id):
    return listing_model.get_listing_by_id(listing_id).description


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

@app.route('/listing/<int:listing_id>', methods=['GET', 'POST'])
def listing_details(listing_id):
    """
    The route shows the listing details of the given listing ID
    :param listing_id:
    """
    if listing_model.get_listing_by_id(listing_id).is_available == 'false':
        flash("That listing is out for loan and not available for bidding", "error")
        return redirect(url_for('index'))
    form = BidForm()
    bids = bid_model.get_bids_under_listing(listing_id)
    # check if avail is false then redirect depending on whether the user is the owner or not
    listing = listing_model.get_listing_by_id(listing_id)
    owner = user_model.get_user_by_id(listing.owner_id)
    if request.method == 'POST':
        if not current_user.is_authenticated:  # check if user is logged in to send a post request
            return login_manager.unauthorized()
        if 'bidder_id' in request.form:  # update bid
            bidder_id = int(request.form.get('bidder_id'))
            new_price = float(request.form.get('bid_price'))
            bid_to_update = [bid for bid in bids if bid.bidder_id == bidder_id][0]
            if bid_to_update.update_bid(price=new_price):
                flash("Updated your bid successfully", "success")
            else:
                flash("Updated failed", "error")

        elif form.validate_on_submit():  # create new bid
            new_bid = bid_model.Bid(current_user.id, listing_id, datetime.now(), form.price.data)
            if new_bid.create_bid():
                flash("Your bid has been placed", "success")
            else:
                flash("Placing of bid has failed", "error")

        return redirect(url_for('listing_details', listing_id=listing_id))
    return render_template('listing.html', listing=listing, bids_under_this_listing=bids, owner=owner, form=form)


@app.route('/generate_loan/<int:bidder_id>/<int:listing_id>/<string:listing_name>', methods=['GET', 'POST'])
@login_required
def generate_loan(bidder_id, listing_id, listing_name):
    form = GenerateLoanForm()
    if request.method == 'POST' and form.validate_on_submit():
        bid_date = bid_model.get_bid_under_listing_and_bidder(bidder_id, listing_id).bid_date
        borrow_date = datetime.now()
        return_date = datetime.combine(form.return_date.data, datetime.now().time())
        loan_model.Loan(bidder_id, listing_id, bid_date, borrow_date, return_date, form.return_loc.data,
                        form.pickup_loc.data).create_loan()  # check if loan was created and flash success
        bid_model.delete_all_bids_of_listing_not_under_bidder(listing_id, bidder_id)
        listing_model.get_listing_by_id(listing_id).update_listing(is_available=False)
        return redirect(url_for('loan_details', listing_id=listing_id))
    return render_template('loan_generation.html', form=form, bidder_id=bidder_id, listing_name=listing_name)


@app.route('/loan/<int:listing_id>', methods=['GET', 'POST'])
@login_required
def loan_details(listing_id):
    if request.method == 'POST':
        loan_model.delete_loan_of_listing(listing_id)
        bid_model.delete_bids_of_listing(listing_id)
        listing_model.get_listing_by_id(listing_id).update_listing(is_available=True)
        flash("Loan returned", "success")
        return redirect(url_for('index'))
    current_loan = loan_model.get_loan_of_listing(listing_id)  # Need to check if None Type
    return render_template('loan.html', loan=current_loan)
