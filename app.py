from flask import Flask, request, jsonify
from database import db
from models import User, FinancialRecord
from auth import role_required
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required
)
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['JWT_SECRET_KEY'] = 'secretkey'

db.init_app(app)
jwt = JWTManager(app)

# ---------- INIT DB ----------
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username="admin").first():
        admin = User(username="admin", role="admin")
        db.session.add(admin)
        db.session.commit()

@app.route('/')
def home():
    return "Finance Backend API Running "
# ---------- LOGIN ----------
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get("username")
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    token = create_access_token(identity=str(user.id), additional_claims={
        "role": user.role
    })

    return jsonify(access_token=token)

# ---------- USER MANAGEMENT ----------
@app.route('/users', methods=['POST'])
@jwt_required()
@role_required('admin')
def create_user():
    data = request.json

    if not data.get("username") or not data.get("role"):
        return jsonify({"error": "Missing fields"}), 400

    user = User(
        username=data['username'],
        role=data['role']
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created"})

@app.route('/users', methods=['GET'])
@jwt_required()
@role_required('admin')
def get_users():
    users = User.query.all()
    return jsonify([
        {"id": u.id, "username": u.username, "role": u.role}
        for u in users
    ])

# ---------- RECORDS ----------
@app.route('/records', methods=['POST'])
@jwt_required()
@role_required('admin')
def create_record():
    data = request.json

    if data['type'] not in ['income', 'expense']:
        return jsonify({"error": "Invalid type"}), 400

    record = FinancialRecord(
        amount=data['amount'],
        type=data['type'],
        category=data.get('category'),
        notes=data.get('notes'),
        date=datetime.strptime(data['date'], "%Y-%m-%d")
    )

    db.session.add(record)
    db.session.commit()

    return jsonify({"message": "Record created"})

@app.route('/records', methods=['GET'])
@jwt_required()
@role_required('admin', 'analyst', 'viewer')
def get_records():
    records = FinancialRecord.query.all()
    return jsonify([
        {
            "id": r.id,
            "amount": r.amount,
            "type": r.type,
            "category": r.category,
            "date": r.date,
            "notes": r.notes
        }
        for r in records
    ])

@app.route('/records/<int:id>', methods=['PUT'])
@jwt_required()
@role_required('admin')
def update_record(id):
    record = FinancialRecord.query.get(id)

    if not record:
        return jsonify({"error": "Not found"}), 404

    data = request.json
    record.amount = data.get('amount', record.amount)
    record.category = data.get('category', record.category)

    db.session.commit()
    return jsonify({"message": "Updated"})

@app.route('/records/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_record(id):
    record = FinancialRecord.query.get(id)

    if not record:
        return jsonify({"error": "Not found"}), 404

    db.session.delete(record)
    db.session.commit()

    return jsonify({"message": "Deleted"})

# ---------- DASHBOARD ----------
@app.route('/dashboard', methods=['GET'])
@jwt_required()
@role_required('admin', 'analyst')
def dashboard():
    records = FinancialRecord.query.all()

    total_income = sum(r.amount for r in records if r.type == 'income')
    total_expense = sum(r.amount for r in records if r.type == 'expense')

    return jsonify({
        "total_income": total_income,
        "total_expense": total_expense,
        "net_balance": total_income - total_expense
    })

# ---------- RUN ----------
if __name__ == '__main__':
    app.run(debug=True)
