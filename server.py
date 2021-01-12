import peeweedbevolve # new; must be imported before models
import os
from flask import Flask, flash, render_template, request, redirect, url_for
from models import db
from models import *

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.before_request
def before_request():
   db.connect()

@app.after_request
def after_request(response):
   db.close()
   return response

@app.cli.command() # new
def migrate(): # new 
   db.evolve(ignore_tables={'base_model'}) # new

@app.route("/")
def index():
    return render_template('index.html')

# STORE
@app.route("/store", methods=["GET"])
def store():
    return render_template("store.html")

@app.route("/store/new", methods=["POST"])
def create_store():
    store = Store(name=request.form['name'])
    if store.save():
        flash("Store has been succesfully added!")
    else:
        flash("Could not be saved!")
    return redirect(url_for('store'))

@app.route("/store/<int:id>", methods=["GET"])
def show_store(id):
    store = Store.get_by_id(id)
    return render_template('store_show.html', store=store)

@app.route("/store/<int:id>/update", methods=["POST"])
def edit_store(id):
    store = Store(
        id=id,
        name=request.form['name']
    )
    if store.save(only=[Store.name]):
        flash("Your store's name has been updated!")
    else:
        flash("Unable to edit store name!")
    return redirect(url_for('show_store', id=id))

@app.route("/stores", methods=["GET"])
def list_stores():
    stores = Store.select()
    return render_template('stores.html', stores=stores)

@app.route("/store/<int:id>/delete", methods=["POST"])
def delete_store(id):
    store = Store.get_by_id(id)
    if store.delete_instance(recursive=True):
        flash("Successfully deleted store!")
    else:
        flash("Unable to delete store!")
    return redirect(url_for('list_stores'))

# WAREHOUSE
@app.route("/warehouse", methods=["GET"])
def warehouse():
    stores = Store.select()
    return render_template("warehouse.html", stores=stores)

@app.route("/warehouse/new", methods=["POST"])
def create_warehouse():
    store = Store.get(
        id=request.form['store_id']
    )
    warehouse = Warehouse(
        location=request.form['location'],
        store=store
    )

    if warehouse.save():
        flash("Your warehouse has been saved!")
    else:
        flash("Your warehouse could not be saved!")
    return redirect(url_for('warehouse'))

@app.route("/warehouse/<int:id>", methods=["GET"])
def show_warehouse(id):
    warehouse = Warehouse.get_by_id(id)
    stores = Store.select()
    return render_template('warehouse_show.html', warehouse=warehouse, stores=stores)

@app.route("/warehouse/<int:id>/update", methods=["POST"])
def update_warehouse(id):
    warehouse = Warehouse(
        id=id,
        location=request.form['location']
    )
    if warehouse.save(only=[Warehouse.location]):
        flash("Your warehouse location has been updated!")
    else:
        flash("Could not update warehouse's location!")
    return redirect(url_for('show_warehouse', id=id))

@app.route("/warehouses", methods=["GET"])
def list_warehouses():
    warehouses = Warehouse.select()
    return render_template("warehouses.html", warehouses=warehouses)

@app.route("/warehouse/<int:id>/delete", methods=["POST"])
def delete_warehouse(id):
    warehouse = Warehouse.get_by_id(id)
    if warehouse.delete_instance():
        flash("Deleted warehouse!")
    else:
        flash("Could not delete warehouse!")
    return redirect(url_for('list_warehouses'))

# PRODUCT
@app.route("/product", methods=["GET"])
def product():
    return render_template("product.html")

if __name__ == '__main__':
   app.run()