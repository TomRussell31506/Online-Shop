from flask import Flask, render_template, request, abort, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config["SECRET_KEY"] = "top secret password don't tell anyone this"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.sqlite3"
db = SQLAlchemy(app)

class Cheeses(db.Model):
    __tablename__ = "cheeses"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), index=True, unique=True)
    price = db.Column(db.String(8))
    description = db.Column(db.Text)
    impact = db.Column(db.String(32))

class QuantityForm(FlaskForm):
    quantity = IntegerField("How many to add to basket: ",validators = [DataRequired(),NumberRange(0,50)])
    submit = SubmitField("Add to basket!")

class SortForm(FlaskForm):
    order = SelectField("Sort by:", choices=[
        ("name","Name"),
        ("price","Price"),
        ("impact","Environmental Impact")
    ])
    submit = SubmitField("Update")

class paymentForm(FlaskForm):
    card_num = StringField("Card Number:", validators = [DataRequired(), Length(min=16, max=16)])
    cvc = StringField("CVC:", validators = [DataRequired(), Length(min=3, max=3)])
    expiry_date = StringField("Expiry date (MM/YY):", validators = [DataRequired(), Length(min=5,max=5)])
    name_on_card = StringField("Name on card:", validators = [DataRequired()])
    submit = SubmitField("Purchase")

class removeButton(FlaskForm):
    submit = SubmitField("Remove")

def get_object_with_attribute(attribute_value, attribute_name, object_list):

    for item in object_list:
        if getattr(item, attribute_name) == str(attribute_value):
            return item
        

@app.route("/", methods = ["GET", "POST"])
def galleryPage():
    cheeses = Cheeses.query.all()

    list_cheese_names = []
    for cheese in cheeses:
        list_cheese_names.append(cheese.name)
    
    list_cheese_prices = []
    for cheese in cheeses:
        list_cheese_prices.append(cheese.price)
    for i in range(0, len(list_cheese_prices)):
        list_cheese_prices[i] = int(list_cheese_prices[i])

    list_cheese_impacts = []
    for cheese in cheeses:
        list_cheese_impacts.append(cheese.impact)
    for i in range(0, len(list_cheese_impacts)):
        list_cheese_impacts[i] = int(list_cheese_impacts[i])

    # Sort the cheeses according to the output of the sort form, default to sort by name
    form = SortForm()
    ordered_cheeses = []
    if form.validate_on_submit():
        chosen_order = form.order.data
        if chosen_order == "name":
            list_cheese_names.sort()
            for cheese in list_cheese_names:
                ordered_cheeses.append(get_object_with_attribute(cheese, "name", cheeses))
        elif chosen_order == "price":
            list_cheese_prices.sort()
            for cheese in list_cheese_prices:
                ordered_cheeses.append(get_object_with_attribute(cheese, "price", cheeses))
        elif chosen_order == "impact":
            print(list_cheese_impacts)
            list_cheese_impacts.sort()
            print(list_cheese_impacts)
            for cheese in list_cheese_impacts:
                ordered_cheeses.append(get_object_with_attribute(cheese, "impact", cheeses))
    else:
        list_cheese_names.sort()
        for cheese in list_cheese_names:
            ordered_cheeses.append(get_object_with_attribute(cheese, "name", cheeses))
    
    return render_template('index.html',cheeses = ordered_cheeses, form = form)

@app.route("/cheese/<int:cheeseId>", methods = ["GET", "POST"])
def singleProductPage(cheeseId):
    cheeses = Cheeses.query.all()

    # Do a flask abort if incorrect url
    if cheeseId < 0 or cheeseId > len(cheeses):
        abort(404)

    # Initialise the session if no items in basket
    if "basket" not in session:
        print("New session",flush=True)
        session["basket"] = []
    
    # Store the cheeseID and quantity in the session
    form = QuantityForm()
    if form.validate_on_submit():
        quantity = form.quantity.data  
        session["basket"].append({"id": cheeseId-1 , "quantity": quantity})
        session.modified = True

        return render_template("SingleCheeseBasket.html", cheeses = cheeses[cheeseId-1])
    else:
        return render_template("SingleCheese.html", cheeses = cheeses[cheeseId-1], form=form)
    
@app.route("/basket")
def basketPage():
    cheeses = Cheeses.query.all()
    basket = session.get("basket", [])

    # Turns the useful information into a seperate list of dicts and sums totals
    selected_cheeses = []
    total_price = 0.0
    total_impact = 0.0

    for item in basket:
        cheese = cheeses[item["id"]]
        quantity = item["quantity"]
        price_per_kg = float(cheese.price)
        impact_per_kg = float(cheese.impact)
        selected_cheeses.append({
            "name": cheese.name,
            "price": cheese.price,
            "quantity": item["quantity"]
        })
        total_price += price_per_kg * quantity
        total_impact += impact_per_kg * quantity

    return render_template("basket.html", selected_cheeses=selected_cheeses, total_impact=total_impact, total_price=total_price)

@app.route("/payment", methods = ["GET", "POST"])
def paymentPage():

    form = paymentForm()
    if form.validate_on_submit():
        session.pop("basket", None)     # Clear the basket after user has 'payed' for it
        return render_template("submittedPayment.html")
    else:
        return render_template("payment.html", form = form)


if __name__ == '__main__':
    app.run(debug=True)
