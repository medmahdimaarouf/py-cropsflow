import ast


def parse_value(val_str):
    val_str = val_str.strip()

    # Check for boolean literals
    if val_str == "True":
        return True
    if val_str == "False":
        return False

    # Try to evaluate arithmetic expressions safely using ast
    try:
        node = ast.parse(val_str, mode='eval')
        # Only allow safe nodes: numbers, operators, expressions
        allowed_nodes = (
            ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num,
            ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow,
            ast.Load, ast.USub, ast.UAdd, ast.Constant, ast.Call
        )
        if all(isinstance(n, allowed_nodes) for n in ast.walk(node)):
            # Evaluate safely using eval but restrict builtins
            return eval(val_str, {"__builtins__": None}, {})
    except Exception:
        pass

    # Fallback: try int
    try:
        return int(val_str)
    except ValueError:
        pass

    # Fallback: try float
    try:
        return float(val_str)
    except ValueError:
        pass

    # Otherwise return as string
    return val_str
