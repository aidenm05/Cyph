from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cyph.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define your model
class Cyph(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    strain = db.Column(db.String(80), nullable=False)
    provider = db.Column(db.String(80), nullable=False)
    bowls = db.Column(db.Integer, nullable=False)
    participants = db.Column(db.String(200), nullable=False)

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    buyer = db.Column(db.String(100))
    amount = db.Column(db.Float)
@app.route('/')
def index():
    cyphs = Cyph.query.all()
    cyph_count = len(cyphs)  # Get the count of cyphs
    purchases = Purchase.query.all()
    return render_template('index.html', cyphs=cyphs, purchases=purchases, cyph_count=cyph_count)

@app.route('/add_cyph', methods=['GET', 'POST'])
def add_cyph():
    if request.method == 'POST':
        strain = request.form['strain']
        provider = request.form['provider']
        bowls = int(request.form['bowls'])
        participants = request.form['participants']

        new_cyph = Cyph(strain=strain, provider=provider, bowls=bowls, participants=participants)
        db.session.add(new_cyph)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_cyph.html')

@app.route('/add_purchase', methods=['GET', 'POST'])
def add_purchase():
    if request.method == 'POST':
        buyer = request.form['buyer']
        amount = float(request.form['amount'])

        new_purchase = Purchase(buyer=buyer, amount=amount)
        db.session.add(new_purchase)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_purchase.html')

@app.route('/summary')
def summary():
    purchases = Purchase.query.all()
    total_spent = sum(p.amount for p in purchases)
    breakdown = {p.buyer: 0 for p in purchases}
    for p in purchases:
        breakdown[p.buyer] += p.amount

    return render_template('summary.html', total_spent=total_spent, breakdown=breakdown)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
