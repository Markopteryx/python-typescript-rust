def calculate_sum(a: float, b: float) -> float:
    # Incorrect indentation and unnecessary semicolon
    return a + b


class ExampleClass:
    def __init__(self, name):
        self.name = name  # Missing spaces around =

    def say_hello(self):
        print("Hello, " + self.name + "!")  # Prefer f-strings and add spaces for readability


# Unused import


# Comparing things incorrectly
def check_values():
    x = 5
    if x == None:  # Should use `is` for None comparison
        print("x is None")
    else:
        print("x is not None")


calculate_sum(5, 10)
example = ExampleClass("World")
example.say_hello()
check_values()

# Inconsistent use of quotes
single_quoted_string = "Hello, World"
double_quoted_string = "Hello, World"

# Unused variable
unused_var = "I'm not used"


# Mutable default argument
def add_to_list(item, target_list=[]):
    target_list.append(item)
    return target_list
