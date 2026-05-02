from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///expenses.db'
app.config['SECRET_KEY'] = 'secret123'

db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    amount = db.Column(db.Float)
    category = db.Column(db.String(50))

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

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

    return jsonify({"message": "Added"})

@app.route("/delete_expense/<int:id>", methods=["DELETE"])
def delete_expense(id):
    expense = Expense.query.get(id)
    db.session.delete(expense)
    db.session.commit()

    return jsonify({"message": "Deleted"})

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)