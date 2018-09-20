import os
from app import create_app, ItemForm
import db
from flask import render_template, session, redirect, url_for, g, flash, request, jsonify
from datetime import datetime
import json

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

# @app.route('/edit', methods=['GET'])
# def edit_item():
#     itemdict = {
#         "name": "hello",
#         "desc": "he",
#         "price": 2.0
#     }
#     item = Item(**itemdict)
#     form = ItemForm(obj=item)
#     return render_template('index.html', form=form)
#

class Item:
    def __init__(self, item_name, description, price):
        self.item_name = item_name
        self.description = description
        self.price = price


@app.route('/updateItem', methods=['POST'])
def updateItem():
    form = ItemForm()
    all_items = db.get_all_items()

    if request.method == 'POST':
        data = request.get_json()

        oldItem = Item(**data['oldItem'])
        newItem = Item(**data['newItem'])

        if not db.update_item(newItem.item_name, newItem.description, newItem.price, oldItem.item_name):
            flash('Update failed!', "error")
            app.logger.warning("Update failed")
        else:
            flash("Successfully updated an item!", "success")

        return redirect(url_for('index'))

    return render_template('index.html', items=all_items, form=form, current_time=datetime.utcnow())

    # return json.dumps({'status':'OK'})

