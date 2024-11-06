from utils.email_utils import is_valid_email

def validate_student_data(data):
    errors = {}
    if 'name' not in data or not data['name']:
        errors['name'] = "Name is required."
    if 'age' not in data or not isinstance(data['age'], int) or data['age'] <= 0:
        errors['age'] = "Age must be a positive integer."
    if 'email' not in data or not is_valid_email(data['email']):
        errors['email'] = "A valid email is required."
    
    return errors
