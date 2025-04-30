from flask import Flask, render_template, request, abort, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = "top secret password don't tell anyone this"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
db = SQLAlchemy(app)

class QuantityForm(FlaskForm):
    quantity = IntegerField('How many to add to basket: ',validators = [DataRequired(),NumberRange(0,50)])
    submit = SubmitField('Add to basket!')

cheeses = [
    { "name": "Cheddar", "price": "£4/kg", "description": "Cheddar is a popular, firm cheese originating from Cheddar, England.", "id":"0" , "impact":"10kg carbon emissions"},
    { "name": "Gouda", "price": "£5/kg", "description": "Gouda is a semi-hard Dutch cheese with a smooth, creamy texture and a sweet, nutty flavor that intensifies as it ages.","id":"1", "impact":"9kg carbon emissions" },
    { "name": "Mozzarella", "price": "£6/kg", "description": "Mozzarella is a soft, mild and stretchy Italian cheese, known for its fresh, milky flavor and excellent melting properties.", "id":"2", "impact":"11kg carbon emissions" },
    { "name": "Edam", "price":"£8/kg", "description": "Edam is a mild, slightly nutty Dutch cheese with a smooth texture and a distinctive red wax coating.", "id":"3", "impact":"7kg carbon emissions"}
]

@app.route('/')
def galleryPage():
    return render_template('index.html',cheeses = cheeses)

@app.route('/cheese/<int:cheeseId>', methods = ["GET", "POST"])
def singleProductPage(cheeseId):
    # Do a flask abort if incorrect url
    if cheeseId < 0 or cheeseId >= len(cheeses):
        abort(404)

    # Initialise the session if no items in basket
    if 'basket' not in session:
        print("New session",flush=True)
        session['basket'] = []
    
    # Store the cheeseID and quantity in the session
    form = QuantityForm()
    if form.validate_on_submit():
        quantity = form.quantity.data  
        session['basket'].append({'id': cheeseId, 'quantity': quantity})
        session.modified = True

        return render_template('SingleCheeseBasket.html', cheeses = cheeses[cheeseId])
    else:
        return render_template('SingleCheese.html', cheeses = cheeses[cheeseId], form=form)
    
@app.route('/basket')
def basketPage():
    basket = session.get('basket', [])

    # Turns the useful information into a seperate list of dicts
    # and sum totals
    selected_cheeses = []
    total_price = 0.0
    total_impact = 0.0

    for item in basket:
        cheese = cheeses[item['id']]
        quantity = item['quantity']
        price_per_kg = float(cheese['price'].replace('£', '').replace('/kg', ''))
        impact_per_kg = float(cheese['impact'].replace('kg carbon emissions', ''))
        selected_cheeses.append({
            'name': cheese['name'],
            'price': cheese['price'],
            'quantity': item['quantity']
        })
        total_price += price_per_kg * quantity
        total_impact += impact_per_kg * quantity

    return render_template('basket.html', selected_cheeses=selected_cheeses, total_impact=total_impact, total_price=total_price)

if __name__ == '__main__':
    app.run(debug=True)
