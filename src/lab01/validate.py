# Validate

min_age = 16

def validate_id(value):
    if not isinstance(value, int):
        raise TypeError("ID must be integer")
    if value < 0: 
        raise ValueError("ID can not be negative")
    
def validate_name(value):
    if not isinstance(value, str):
        raise TypeError("Name must be string")
    if not value.strip():
        raise ValueError("Name can not be empty")
    
def validate_age(value, min_age):
    if not isinstance(value, int):
        raise TypeError("Age must be integer")
    if value < min_age:
        raise ValueError(f"Age must be at least {min_age}")
    
def validate_weight(value):
    if not isinstance(value, float):
        raise TypeError("Weight must be float")
    if value <= 0:
        raise ValueError("Weight can not be negative or zero")
    
def validate_height(value):
    if not isinstance(value, float):
        raise TypeError("Height must be float")
    if value <= 0:
        raise ValueError("Height can not be negative")
    
def validate_status(value):
    if not isinstance(value, bool):
        raise TypeError("Status must be boolean")

def validate_num_visiting(value):
    if not isinstance(value, int):
        raise TypeError("Numbet of visiting must be an integer")
    if value < 0:
        raise ValueError("Numbet of visiting can not be negative")
    
def validate_paid(value):
    if not isinstance(value, bool):
        raise TypeError("Payment must be boolean")  