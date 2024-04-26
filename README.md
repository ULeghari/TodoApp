# TodoApp

TodoApp is a web application to help user manage their tasks efficiently. Users can create, Update and Delet tasks. It has been made with Django REST Framework.

## Features

1. User Registration
2. User Authentication
3. Create Todo Items
4. Update Todo Items
5. Delete Todo Items

## Technologies Used

Django REST Framework

## Installation

1. Clone the repository
2. Navigate to the project directory
3. Install the project dependencies using "pip install -r requirements.txt"
4. Run the migrations to create database tables
5. Start the Django development server usning "python manage.py runserver"

## Model

### ToDo Model

1. user (ForeignKey to User): The user who owns the ToDo item.
2. todo_name (CharField): Name of the ToDo item.
3. description (TextField): The description of the ToDo item.
4. status (BooleanField): Status of the ToDo item (True: completed, False: not completed).
5. Relationships: Many-to-one relationship with the User model.

## Views

1. UserRegistrationAPIView: Handles user registration.
2. UserLoginAPIView: Handles user login.
3. UserLogoutAPIView: Handles user logout.
4. ToDoListCreateAPIView: Handles listing and creation of ToDo items.
5. ToDoDetailAPIView: Handles retrieval, update, and deletion of ToDo items.

## API endpoints

1. /register/: User registration.
2. /login/: User login.
3. /logout/: User logout.
4. /todos/: List and create ToDo items.
5. /todos/<str:name>/: Retrieve, update, and delete ToDo items by name.

## ToDoSerializer

The ToDoSerializer serializes and deserializes ToDo objects.

## Testing
Unit tests are included in the project to ensure the functionality of API endpoints.
