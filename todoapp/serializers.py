from rest_framework import serializers
from .models import ToDo

class ToDoSerializer(serializers.ModelSerializer):
    """
        Serializer: ToDoSerializer

        Serialized Fields:
        - id: The id of the ToDo item.
        - user: The user who owns the ToDo item.
        - todo_name: Name of the ToDo item.
        - description: Description of the ToDo item.
        - status: Status of the ToDo item.
    """

    class Meta:
        model = ToDo
        fields = ['id', 'user', 'todo_name', 'description', 'status']
