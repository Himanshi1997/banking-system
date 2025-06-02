# 🏦 Django Banking System

A Django REST Framework-based banking system supporting:
- Zero Balance, Student, and Regular Savings Accounts
- Account-type-specific business rules
- Deposits, Withdrawals, Transfers, Transaction Reversals
- Audit Trail & Transaction History
- Fully Dockerized setup
- Postman/OpenAPI documentation

---

## 📦 Features

### ✅ Account Types & Rules
- **Zero Balance Account**:
  - Max 4 withdrawals/month
  - No minimum balance
- **Student Account**:
  - Age: 18–25
  - Max 4 withdrawals/month
  - ₹10,000 monthly deposit limit
  - ₹1,000 minimum balance
- **Regular Savings Account**:
  - 10 free withdrawals/month; ₹5 fee after
  - ₹50,000 monthly deposit limit (KYC needed above this)
  - ₹5,000 average 90-day balance requirement (logic placeholder)

### ✅ Transactions
- Deposit, Withdraw, Transfer
- Business rule enforcement per account type
- Transaction fee calculation (for Regular Accounts)
- Reversal support for all transaction types

### ✅ Audit Trail
- Every action (deposit, withdrawal, transfer, reversal) logged

---

## 🚀 Setup Instructions

### 🔧 Local Development
```bash
# 1. Clone the repository
https://github.com/Himanshi1997/banking-system.git
cd banking-system

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Run server
python manage.py runserver
```

---

### 🐳 Docker Setup
```bash
# 1. Clone the repository
https://github.com/Himanshi1997/banking-system.git
cd banking-system

# 2. Build Docker image & run
docker-compose up -d --build

App runs at: [http://localhost:8000](http://localhost:8000)
```
---

## 🔌 API Collection & Endpoints

### Postman Collection: postman_collection.json

| Method | URL                        | Description                      |
|--------|-----------------------------|----------------------------------|
| POST   | `/accounts/`     | Create a new account             |
| GET    | `/accounts/`        | List user’s accounts             |
| POST   | `/transactions/deposit/`            | Deposit funds                    |
| POST   | `/transactions/withdraw/`           | Withdraw funds                   |
| POST   | `/transactions/transfer/`           | Transfer between accounts        |
| GET    | `/transactions/`       | Get transaction history          |
      |

Use token-based.

---

## 🧪 Tests

Run tests with:
```bash
python manage.py test
```
Includes:
- Unit tests for business rules & services
- API tests for account and transaction flows

---

## 📁 Project Structure

```bash
banking_system/
├── accounts/               # Account models, views, rules
├── transactions/           # Transaction logic & APIs
├── docker/                 # Docker & setup
├── users/         
├── manage.py
└── requirements.txt
```
---
