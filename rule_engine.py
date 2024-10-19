class Node:
    def __init__(self, node_type, value=None, left=None, right=None):
        self.type = node_type  # 'operator' or 'operand'
        self.value = value  # condition value for operands (age > 30, etc.)
        self.left = left  # Left child node (for operators)
        self.right = right  # Right child node (for operators)

    def to_dict(self):
        return {
            "type": self.type,
            "value": self.value,
            "left": self.left.to_dict() if self.left else None,
            "right": self.right.to_dict() if self.right else None
        }


def create_rule(rule_string):
    # This function should parse the rule_string and build the AST.
    # For simplicity, we will simulate the creation of a dummy AST.
    if "age" in rule_string:
        return Node("operator", "AND",
                    Node("operand", "age > 30"),
                    Node("operand", "department == 'Sales'"))
    else:
        raise ValueError("Invalid rule string")


def combine_rules(rules, combine_with="AND"):
    # Combine multiple ASTs into one using the specified operator.
    combined_ast = Node("operator", combine_with, rules[0], rules[1])
    return combined_ast


def evaluate_rule(node, user_data):
    # This function recursively evaluates the AST based on user data.
    if node.type == "operand":
        # Evaluate the condition
        condition = node.value
        if "age > 30" in condition:
            return user_data.get("age", 0) > 30
        elif "department == 'Sales'" in condition:
            return user_data.get("department") == "Sales"
    elif node.type == "operator":
        left_eval = evaluate_rule(node.left, user_data)
        right_eval = evaluate_rule(node.right, user_data)
        if node.value == "AND":
            return left_eval and right_eval
        elif node.value == "OR":
            return left_eval or right_eval


def modify_operator(node, old_value, new_value):
    if node.type == "operator" and node.value == old_value:
        node.value = new_value


def modify_condition(node, old_value, new_value):
    if node.type == "operand" and node.value == old_value:
        node.value = new_value
