from flask import Flask, render_template, request, abort
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = "top secret password don't tell anyone this"

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
    if cheeseId < 0 or cheeseId >= len(cheeses):
        abort(404)
    form = QuantityForm()
    if form.validate_on_submit():
        return render_template('SingleCheeseBasket.html', cheeses = cheeses[cheeseId])
    else:
        return render_template('SingleCheese.html', cheeses = cheeses[cheeseId], form = form)
    
@app.route('/basket')
def basketPage():
    return render_template('basket.html', cheeses = cheeses)

if __name__ == '__main__':
    app.run(debug=True)
