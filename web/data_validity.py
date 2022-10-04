
def check_posted_data(data, fxn_name):
    func_methods = ["add", "subtract", "multiply", "division"]
    if fxn_name in func_methods:
        return 301 if "x" not in data or "y" not in data else 200

