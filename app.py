import logging
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from db import SessionLocal, Rule, User
from rule_engine import create_rule, combine_rules, evaluate_rule, modify_operator, modify_condition

app = FastAPI()

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Request models for FastAPI
class RuleRequest(BaseModel):
    rule_string: str

class CombineRequest(BaseModel):
    rule_ids: list[int]
    operator: str = "AND"

class EvaluationRequest(BaseModel):
    rule_id: int
    user_data: dict

class ModifyRequest(BaseModel):
    rule_id: int
    operation: str  # "modify_operator" or "modify_condition"
    old_value: str
    new_value: str

# API to create a rule
@app.post("/rule/create")
async def create_rule_api(rule_request: RuleRequest, db: Session = Depends(get_db)):
    try:
        rule_ast = create_rule(rule_request.rule_string)
        
        # Convert rule_ast to dictionary
        rule_ast_serialized = rule_ast.to_dict()  # Assuming rule_ast is a Node object

        db_rule = Rule(rule_ast=rule_ast_serialized)  # JSON-serializable format
        db.add(db_rule)
        db.commit()
        db.refresh(db_rule)
        return {"rule_id": db_rule.id, "rule_ast": db_rule.rule_ast}
    except Exception as e:
        logging.error(f"Error while creating rule: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# API to combine rules
@app.post("/rule/combine")
async def combine_rules_api(combine_request: CombineRequest, db: Session = Depends(get_db)):
    rule_asts = [
        db.query(Rule).filter(Rule.id == rid).first()
        for rid in combine_request.rule_ids
    ]
    
    # Ensure that all rules were found
    rule_asts = [rule for rule in rule_asts if rule is not None]
    if len(rule_asts) != len(combine_request.rule_ids):
        raise HTTPException(status_code=404, detail="One or more rules not found")
    
    combined_ast = combine_rules(rule_asts, combine_with=combine_request.operator)
    return {"combined_rule_ast": combined_ast.to_dict()}

# API to evaluate a rule
@app.post("/rule/evaluate")
async def evaluate_rule_api(eval_request: EvaluationRequest, db: Session = Depends(get_db)):
    db_rule = db.query(Rule).filter(Rule.id == eval_request.rule_id).first()
    if not db_rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    result = evaluate_rule(db_rule.rule_ast, eval_request.user_data)
    return {"result": result}

# API to modify a rule
@app.patch("/rule/modify")
async def modify_rule_api(modify_request: ModifyRequest, db: Session = Depends(get_db)):
    db_rule = db.query(Rule).filter(Rule.id == modify_request.rule_id).first()
    if not db_rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    
    try:
        if modify_request.operation == "modify_operator":
            modify_operator(db_rule.rule_ast, modify_request.old_value, modify_request.new_value)
        elif modify_request.operation == "modify_condition":
            modify_condition(db_rule.rule_ast, modify_request.old_value, modify_request.new_value)
        else:
            raise HTTPException(status_code=400, detail="Invalid operation type")
        db.commit()
        return {"modified_rule_ast": db_rule.rule_ast}
    except Exception as e:
        logging.error(f"Error while modifying rule: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
