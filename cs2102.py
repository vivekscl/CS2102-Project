import os
from app import create_app, ItemForm, LoginForm, SignUpForm, BidForm, GenerateLoanForm, login_manager, SearchForm
from flask_login import login_required, logout_user, login_user, current_user
from models import user as user_model, listing as listing_model, bid as bid_model, loan as loan_model, tag as tag_model, listing_tag as listing_tag_model
from werkzeug.security import generate_password_hash
from flask import render_template, redirect, url_for, g, flash, request
from datetime import datetime
from db import DatabaseCursor

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

# =========== ERROR HANDLERS ============= #
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# =========== TEMPLATE FILTERS =========== #
@app.template_filter('convert_bidder_id_to_name')
def convert_bidder_id_to_name(bidder_id):
    return user_model.get_user_by_id(bidder_id).name


@app.context_processor
def get_listing_to_description():
    def listing_description(listing_name, owner_id):
        return listing_model.get_listing(listing_name, owner_id).description
    return dict(get_listing_to_description=listing_description)
# ======================================== #


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
        user = user_model.User(None, form.username.data, form.email.data, form.name.data,
                               generate_password_hash(form.password.data), form.phonenumber.data)
        user.create_user()
        flash("You can now login", "success")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/user', methods=['GET'])
@login_required
def user_page():
    listings = listing_model.get_listings_with_tags(current_user.id)
    loans = loan_model.get_loans_under_bidder(current_user.id)
    available = []
    not_available = []

    for listing in listings:
        print(listing.tag_name)
        if listing.is_available == 'true':
            available.append(listing)
        else:
            not_available.append(listing)
    return render_template('user.html', available=available, not_available=not_available, loans=loans)


@app.route('/', methods=['GET', 'POST'])
def index():
    expensive_listings = listing_model.get_expensive_listings()
    popular_listings = listing_model.get_popular_listings()

    # form = SearchForm()
    # if request.method == 'POST' and form.validate_on_submit():
    #     return redirect(url_for('search_results', type=form.select.data, query=form.search.data))

    return render_template('index.html', current_time=datetime.utcnow(),
                           e_listings=expensive_listings, p_listings=popular_listings)


@app.route('/search_results', defaults={'type': '', 'query': ''})
@app.route('/search_results/<string:type>/<string:query>')
def search_results(type, query):

    if type == 'all':
        listing = listing_model.get_all_listing()
    elif type == 'tag':
        listing = listing_model.get_listings_by_tag_name('%' + query + '%')
    elif type == 'owner':
        listing = listing_model.get_listings_by_owner_name('%' + query + '%')
    else:
        flash('No results found!')

    return render_template('search_results.html', listing=listing)
    

@app.route('/listing/create', methods=['GET', 'POST'])
@login_required
def create_listing():

    form = ItemForm()
    current_time=datetime.utcnow()

    # If a post request is sent, validate the form and insert the new listing into the db using listing_model.
    if request.method == 'POST':
        if form.validate_on_submit():
            owner_id = current_user.id
            listing_name = form.item_name.data
            tag_id = form.tags.data
            listing = listing_model.Listing(listing_name, owner_id, form.description.data,
                                            current_time, True)
            if listing.create_listing():
                # Inserts record to listing_tag table accordingly
                listing_tag = listing_tag_model.ListingTag(tag_id, listing_name, owner_id)
                if listing_tag.insert_listing_tag():
                    flash("Successfully added a new listing.", "success")
                    return redirect(url_for('index'))
            else:
                flash('You have created this listing before, unable to add.', "error")
                app.logger.warning("Insert failed") # to-do provide error msg for diff insertion error

    return render_template('create_listing.html', form=form, current_time=current_time)


@app.route('/listing/<string:listing_name>/<int:owner_id>', methods=['GET', 'POST'])
def listing_details(listing_name, owner_id):

    if listing_model.get_listing(listing_name, owner_id).is_available == 'false':
        flash("That listing is out for loan and not available for bidding", "error")
        return redirect(url_for('index'))
    form = BidForm()
    bids = bid_model.get_bids_under_listing(listing_name, owner_id)
    # check if avail is false then redirect depending on whether the user is the owner or not
    listing = listing_model.get_listing(listing_name, owner_id)
    owner = user_model.get_user_by_id(owner_id)

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
            new_bid = bid_model.Bid(current_user.id, listing_name, owner_id, datetime.now(), form.price.data)
            if new_bid.create_bid():
                flash("Your bid has been placed", "success")
            else:
                flash("Placing of bid has failed", "error")

        return redirect(url_for('listing_details', listing_name=listing_name, owner_id=owner_id))
    return render_template('listing.html', listing=listing, bids_under_this_listing=bids, owner=owner, form=form)


@app.route('/generate_loan/<int:bidder_id>/<string:listing_name>/<int:owner_id>', methods=['GET', 'POST'])
@login_required
def generate_loan(bidder_id, listing_name, owner_id):
    """
    generate_loan
    When a loan is generated i.e. a new loan is inserted into the loan table,
1. delete all bids for the listing except the winning one and
2. mark the listing as unavailable
    :param bidder_id:
    :param listing_name:
    :param owner_id:
    :return:
    """
    form = GenerateLoanForm()
    if request.method == 'POST' and form.validate_on_submit():
        bid_date = bid_model.get_bid_under_listing_and_bidder(bidder_id, listing_name, owner_id).bid_date
        borrow_date = datetime.now()
        return_date = datetime.combine(form.return_date.data, datetime.now().time())
        loan_model.Loan(bidder_id, listing_name, owner_id, bid_date, borrow_date, return_date, form.return_loc.data,
                        form.pickup_loc.data).create_loan()  # check if loan was created and flash success
        return redirect(url_for('loan_details', listing_name=listing_name, owner_id=owner_id))
    return render_template('loan_generation.html', form=form, bidder_id=bidder_id, listing_name=listing_name)


@app.route('/loan/<string:listing_name>/<int:owner_id>', methods=['GET', 'POST'])
@login_required
def loan_details(listing_name, owner_id):
    if current_user.id != owner_id:
        flash("You are not the owner of that listing", "error")
        return redirect(url_for('index'))
    if request.method == 'POST':
        if not current_user.is_authenticated:  # check if user is logged in to send a post request
            return login_manager.unauthorized()
        loan_model.delete_loan_of_listing(listing_name, owner_id)
        flash("Loan returned", "success")
        return redirect(url_for('index'))
    current_loan = loan_model.get_loan_of_listing(listing_name, owner_id)  # Need to check if None Type
    return render_template('loan.html', loan=current_loan)
