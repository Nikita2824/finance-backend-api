from database import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)  # viewer, analyst, admin
    is_active = db.Column(db.Boolean, default=True)

class FinancialRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(10), nullable=False)  # income/expense
    category = db.Column(db.String(50))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.String(200))