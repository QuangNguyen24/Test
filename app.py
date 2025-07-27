import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer)
    quantity = db.Column(db.Integer, default=1)

products = [
    {"id": 1, "name": "Áo Thun", "price": 200000, "image": "/static/images/ao-thun.jpg"},
    {"id": 2, "name": "Quần Jeans", "price": 400000, "image": "/static/images/quan-jeans.jpg"},
    {"id": 3, "name": "Áo Khoác", "price": 500000, "image": "/static/images/ao-khoac.jpg"},
]

@app.route('/')
def index():
    return render_template('index.html', products=products)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    item = CartItem.query.filter_by(product_id=product_id).first()
    if item:
        item.quantity += 1
    else:
        item = CartItem(product_id=product_id)
        db.session.add(item)
    db.session.commit()
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    items = CartItem.query.all()
    cart_products = []
    total_price = 0
    for item in items:
        product = next((p for p in products if p["id"] == item.product_id), None)
        if product:
            total = product["price"] * item.quantity
            cart_products.append({
                "name": product["name"],
                "price": product["price"],
                "quantity": item.quantity,
                "total": total
            })
            total_price += total
    return render_template('cart.html', cart_products=cart_products, total_price=total_price)

@app.route('/checkout')
def checkout():
    db.session.query(CartItem).delete()
    db.session.commit()
    return render_template('checkout.html')

if __name__ == '__main__':
    app.run(debug=True)