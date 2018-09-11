import os
from app import create_app, ItemForm
import db
from flask import render_template, session, redirect, url_for, g, flash, request
from datetime import datetime

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = ItemForm()
    all_items = db.get_all_items()

    # If a post request is sent, validate the form and insert the item into db
    if request.method == 'POST':
        if form.validate_on_submit():
            if not db.insert_item(form.item_name.data, form.description.data, form.price.data):
                flash('That item already exists! Try another one!', "error")
                app.logger.warning("Insert failed due to unique constraint")
            else:
                flash("Successfully added an item!", "success")
            return redirect(url_for('index'))

    return render_template('index.html', items=all_items, form=form, current_time=datetime.utcnow())
