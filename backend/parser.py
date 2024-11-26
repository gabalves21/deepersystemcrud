# Import necessary modules and functions
from config import users, test_connection  
from services.users.user_utils import convert_user
from schemas.user_schema import UserSchema 
from models.user_model import User 
from services.users.user_service import create_user 
import json  

# Function to load users from a file
def load_users_from_file(file_path):
    with open(file_path, 'r') as f: 
        return json.load(f) 

# Function to process and parse user data
def parse_data(data):
    data = load_users_from_file('data.json') 
    results = [] 
    errors = [] 

    # Loop through the "users" in the loaded data
    for user in data.get("users", []): 
        try:
            # Convert raw user data into a transformed structure that matches the expected format
            transformed_data = convert_user(user)  

            user_schema = UserSchema()  
            schema_errors = user_schema.validate(transformed_data)

            # If there are validation errors, add them to the 'errors' list and skip further processing for this user.
            if schema_errors:
                errors.append({"user": user.get("user", "unknown"), "errors": schema_errors}) 
                continue 

            # Create a new user instance from the validated and transformed data
            user_instance = User(**transformed_data) 

            # Save the user instance to the database
            result = create_user(user_instance) 

            results.append(result) 

        except Exception as err: 
            # Add the error details to the 'errors' list
            errors.append({"user": user.get("user", "unknown"), "error": str(err)})  # Capture the error and add it to the errors list.

    # After processing all users, print the results or errors
    if errors: 
        print("Errors", errors)
    else: 
        print("Users created successfully:", results)

# Main block that runs when the script is executed
if __name__ == "__main__":
    parse_data('./data.json')
