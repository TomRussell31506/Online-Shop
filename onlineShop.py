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

class Cheeses(db.Model):
    __tablename__ = 'cheeses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), index=True, unique=True)
    price = db.Column(db.String(8))
    description = db.Column(db.Text)
    impact = db.Column(db.String(32))

class QuantityForm(FlaskForm):
    quantity = IntegerField('How many to add to basket: ',validators = [DataRequired(),NumberRange(0,50)])
    submit = SubmitField('Add to basket!')

@app.route('/')
def galleryPage():
    cheeses = Cheeses.query.all()
    return render_template('index.html',cheeses = cheeses)

@app.route('/cheese/<int:cheeseId>', methods = ["GET", "POST"])
def singleProductPage(cheeseId):
    cheeses = Cheeses.query.all()

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
        session['basket'].append({'id': cheeseId-1, 'quantity': quantity})
        session.modified = True

        return render_template('SingleCheeseBasket.html', cheeses = cheeses[cheeseId-1])
    else:
        return render_template('SingleCheese.html', cheeses = cheeses[cheeseId-1], form=form)
    
@app.route('/basket')
def basketPage():
    cheeses = Cheeses.query.all()
    basket = session.get('basket', [])

    # Turns the useful information into a seperate list of dicts
    # and sum totals
    selected_cheeses = []
    total_price = 0.0
    total_impact = 0.0

    for item in basket:
        cheese = cheeses[item['id']]
        quantity = item['quantity']
        price_per_kg = float(cheese.price.replace('£', '').replace('/kg', ''))
        impact_per_kg = float(cheese.impact.replace('kg carbon emissions', ''))
        selected_cheeses.append({
            'name': cheese.name,
            'price': cheese.price,
            'quantity': item['quantity']
        })
        total_price += price_per_kg * quantity
        total_impact += impact_per_kg * quantity

    return render_template('basket.html', selected_cheeses=selected_cheeses, total_impact=total_impact, total_price=total_price)

if __name__ == '__main__':
    app.run(debug=True)
