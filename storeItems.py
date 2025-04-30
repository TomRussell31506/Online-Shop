from onlineShop import app, db, Cheeses

cheeses = [
    { "name": "Cheddar", "price": "£4/kg", "description": "Cheddar is a popular, firm cheese originating from Cheddar, England.", "impact":"10kg carbon emissions"},
    { "name": "Gouda", "price": "£5/kg", "description": "Gouda is a semi-hard Dutch cheese with a smooth, creamy texture and a sweet, nutty flavor that intensifies as it ages.", "impact":"9kg carbon emissions" },
    { "name": "Mozzarella", "price": "£6/kg", "description": "Mozzarella is a soft, mild and stretchy Italian cheese, known for its fresh, milky flavor and excellent melting properties.", "impact":"11kg carbon emissions" },
    { "name": "Edam", "price":"£8/kg", "description": "Edam is a mild, slightly nutty Dutch cheese with a smooth texture and a distinctive red wax coating.", "impact":"7kg carbon emissions"}
]

with app.app_context():
    db.create_all()
    
    for cheese in cheeses:
        newCheese = Cheeses(name=cheese["name"], price=cheese["price"], description=cheese["description"], impact=cheese["impact"])
        db.session.add(newCheese)
    
    db.session.commit()