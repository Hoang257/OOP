
def _validate_id(value):
    if not isinstance(value, int):
        raise TypeError("ID must be interger")
    if value < 0: 
        raise ValueError("ID can not be negative")
    
    def _validate_name(value):
        if not isinstance(value, str):
            raise TypeError("Name must be sting")
        if not value.strip():
            raise ValueError("Name can not be empty")
    
    def _validate_age(value):
        if not isinstance(value, int):
            raise TypeError("Age must be interger")
        if value < 16:
            raise ValueError("The athlete must be elder 16 y.o")
    
    def _validate_weight(value):
        if not isinstance(value, float):
            raise TypeError("Weight must be float")
        if value < 0:
            raise ValueError("Weight can not be negative")
    
    def _validate_height(value):
        if not isinstance(value, float):
            raise TypeError("Weight must be float")
        if value < 0:
            raise ValueError("Weight can not be negative")
    
    def _validate_status(value):




