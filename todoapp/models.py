from django.db import models
from django.contrib.auth.models import User

class ToDo(models.Model):
    """
        Data Model: ToDo

        Fields:
        - user (ForeignKey to User): The user who owns the ToDo item.
        - todo_name (CharField): Name of the ToDo item.
        - description (TextField): The description of the ToDo item.
        - status (BooleanField): Status of the ToDo item (True: completed, False: not completed).

        Relationships:
        - user: Many-to-one relationship with the User.
    """
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    todo_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.todo_name