from sqlalchemy import create_engine, Column, Integer, String, JSON, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Define PostgresSQL database URL
DATABASE_URL = "postgresql://rule_user:yourpassword@db:5432/rule_engine"

# Set up SQLAlchemy engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Rule table model
class Rule(Base):
    __tablename__ = "rules"
    id = Column(Integer, primary_key=True, index=True)
    rule_ast = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


# User table model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer, nullable=True)
    department = Column(String(50), nullable=True)
    salary = Column(Numeric, nullable=True)
    experience = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


# Create all the tables in the database
Base.metadata.create_all(bind=engine)
