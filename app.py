from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SECRET_KEY'] = 'secret123'

db = SQLAlchemy(app)

# Model
class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    amount = db.Column(db.Float)
    category = db.Column(db.String(50))

# Home route
@app.route("/")
def dashboard():
    return render_template("dashboard.html")

# Get expenses
@app.route("/get_expenses")
def get_expenses():
    expenses = Expense.query.all()
    
    data = []
    for e in expenses:
        data.append({
            "id": e.id,
            "title": e.title,
            "amount": e.amount,
            "category": e.category
        })

    return jsonify(data)

# Add expense
@app.route("/add_expense", methods=["POST"])
def add_expense():
    data = request.json

    new_expense = Expense(
        title=data["title"],
        amount=data["amount"],
        category=data["category"]
    )

    db.session.add(new_expense)
    db.session.commit()

    return jsonify({"message": "Added successfully"})

# Delete expense
@app.route("/delete_expense/<int:id>", methods=["DELETE"])
def delete_expense(id):
    expense = Expense.query.get(id)

    if expense:
        db.session.delete(expense)
        db.session.commit()
        return jsonify({"message": "Deleted successfully"})
    else:
        return jsonify({"error": "Expense not found"}), 404

# Create DB
with app.app_context():
    db.create_all()

# Run app (IMPORTANT FOR RENDER)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)