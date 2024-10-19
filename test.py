from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from db import SessionLocal

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    try:
        # Try to make a simple query
        db.execute("SELECT 1")
        return {"message": "Database connection successful!"}
    except Exception as e:
        return {"error": f"Database connection failed: {str(e)}"}