
# Rule Engine with AST-based Dynamic Rule Evaluation

## Overview
This project implements a **3-tier Rule Engine** application that evaluates user eligibility based on attributes such as age, department, income, and experience. The system uses an **Abstract Syntax Tree (AST)** to represent conditional rules, enabling dynamic creation, combination, and modification of these rules.

The application includes:
1. **FastAPI** as the web framework for API interaction.
2. **SQLAlchemy** with **PostgreSQL** as the database layer for rule and user data storage.
3. **AST-based rule evaluation** to dynamically assess conditions.

---

## Table of Contents

1. [Project Structure](#project-structure)
2. [Design Choices](#design-choices)
3. [Dependencies](#dependencies)
4. [Setup Instructions](#setup-instructions)
5. [Running the Application](#running-the-application)
6. [API Endpoints](#api-endpoints)
7. [Testing the Application](#testing-the-application)

---

## Project Structure

```bash
rule_engine_app/
│
├── app.py                 # FastAPI main app with API endpoints
├── db.py                  # Database models and session handling
├── rule_engine.py         # Core rule engine logic (AST, evaluate, modify)
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker setup for FastAPI
├── docker-compose.yml     # Docker Compose for PostgreSQL and FastAPI
└── README.md              # Project documentation and build instructions
```

---

## Design Choices

### 1. **Abstract Syntax Tree (AST) for Rule Representation**
The system uses an AST to represent rules like `age > 30 AND department = 'Sales'`. This tree-based structure makes it easier to:
- Combine multiple rules.
- Modify existing rules by updating operators or conditions.
- Evaluate user data efficiently using a recursive approach.

### 2. **PostgreSQL for Persistent Rule Storage**
PostgreSQL is used as the database to persist:
- Rules (stored as ASTs in JSON format).
- User attributes (age, department, salary, etc.).

### 3. **API-based Interaction with FastAPI**
FastAPI provides a lightweight API interface to:
- Create rules.
- Combine existing rules.
- Evaluate user data against the rule sets.
- Modify or update rules dynamically.

---

## Dependencies

### 1. **Docker** and **Docker Compose**
This project uses Docker to containerize the PostgreSQL database and the FastAPI application.

### 2. **Python Packages**
The project uses several Python dependencies, which can be installed using `requirements.txt`:

```bash
fastapi==0.88.0
uvicorn==0.22.0
sqlalchemy==2.0.0
psycopg2-binary==2.9.5
pydantic==1.10.5
```

### 3. **PostgreSQL**
A PostgreSQL database is used to store rule data and user information. The database runs inside a Docker container, as defined in the `docker-compose.yml` file.

---

## Setup Instructions

### 1. Clone the repository:
```bash
git clone https://github.com/your-repo/rule-engine-ast.git
cd rule-engine-ast
```

### 2. Install Python dependencies:
Create a virtual environment and install the required dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Set up Docker containers:
Ensure Docker is installed, then run the following command to start both PostgreSQL and the FastAPI app:
```bash
docker-compose up -d
```

This command will:
- Start a **PostgreSQL** container for the database.
- Expose the FastAPI application at [http://localhost:8000](http://localhost:8000).

### 4. Create database tables:
Once the PostgreSQL container is running, the tables for `rules` and `users` can be created automatically when running the FastAPI app by using SQLAlchemy's `Base.metadata.create_all()`.

Alternatively, connect to the PostgreSQL container:
```bash
docker exec -it postgres_db psql -U postgres
```

---

## Running the Application

Once Docker containers are up, the FastAPI application will be available at:

**URL**: `http://localhost:8000`

To access the interactive API documentation, visit:
**Swagger UI**: `http://localhost:8000/docs`

---

## API Endpoints

### 1. Create a Rule
**POST** `/rule/create`

Creates a new rule based on the provided rule string.

**Request Body**:
```json
{
  "rule_string": "age > 30 AND department = 'Sales'"
}
```

**Response**:
```json
{
  "rule_id": 1,
  "rule_ast": {
    "type": "operator",
    "value": "AND",
    "left": {
      "type": "operand",
      "value": "age > 30"
    },
    "right": {
      "type": "operand",
      "value": "department == 'Sales'"
    }
  }
}
```

### 2. Combine Rules
**POST** `/rule/combine`

Combines multiple rules using a logical operator.

**Request Body**:
```json
{
  "rule_ids": [1, 2],
  "operator": "AND"
}
```

**Response**:
```json
{
  "combined_rule_ast": {
    "type": "operator",
    "value": "AND",
    "left": {
      "type": "operator",
      "value": "AND",
      "left": { ... },
      "right": { ... }
    },
    "right": {
      "type": "operator",
      "value": "OR",
      "left": { ... },
      "right": { ... }
    }
  }
}
```

### 3. Evaluate a Rule
**POST** `/rule/evaluate`

Evaluates a rule's AST against provided user data.

**Request Body**:
```json
{
  "rule_id": 1,
  "user_data": {
    "age": 35,
    "department": "Sales",
    "salary": 60000
  }
}
```

**Response**:
```json
{
  "result": true
}
```

### 4. Modify a Rule
**PATCH** `/rule/modify`

Modifies an existing rule (either operator or condition).

**Request Body**:
```json
{
  "rule_id": 1,
  "operation": "modify_operator",
  "old_value": "AND",
  "new_value": "OR"
}
```

**Response**:
```json
{
  "modified_rule_ast": { ... }
}
```

---

## Testing the Application

You can test the endpoints using `cURL` or **Postman**. Examples for each endpoint are provided above.

