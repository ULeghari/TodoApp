from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ToDo
from .serializers import ToDoSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

class UserRegistrationAPIView(APIView):
    """
        API endpoint for user registration.

        Accepted Request Methods:
        - POST

        POST:
        Create a new user.

        Parameters:
        - username: The username for the new user.
        - email: The email for the new user.
        - password: The password for the new user.

        Response:
        {
            "message": "User successfully created"
        }
    """
    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        
        if len(password) < 5:
            return Response({'error': "Password should be at least 5 characters"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({'error': "Username unavailable"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({'message': "User successfully created"}, status=status.HTTP_201_CREATED)

class UserLoginAPIView(APIView):
    """
        API endpoint for login.

        Accepted Request Methods:
        - POST

        POST:
        Authenticate and login the user.

        Parameters:
        - username: Username of the user.
        - password: Password of the user.

        JSON Response:
        {
            "message": "Login successful"
        }
    """
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': "Login successful"})
        else:
            return Response({'error': "Wrong credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class UserLogoutAPIView(APIView):
    """
        API endpoint for logout.
        
        Accepted Request Methods:
        - POST

        Expected Inputs: None

        POST:
        Logout authenticated user.

        JSON Response:
        {
            "message": "Logout successful"
        }
    """
    def post(self, request):
        logout(request)
        return Response({'message': "Logout successful"})


class ToDoListCreateAPIView(APIView):
    """
        API endpoint for creating and retrieving todo items.
        Accepted Request Methods:
        - GET
        - POST

        Expected Inputs for POST:
        - todo_name (string): Name of the todo item.
        - description (string): Description of the todo item.

        GET:
        Get a list of todo items for the authenticated user.

        POST:
        Create a new todo item for authenticated user.

        Parameters for POST:
        - todo_name: Name of the todo item.
        - description: Description of the todo item.

        JSON Response:
        {
            "id": 1,
            "todo_name": "Name",
            "description": "Description of item",
            "status": false,
            "user": 1
        }
    """
    def get(self, request):
        todos = ToDo.objects.filter(user=request.user)
        serializer = ToDoSerializer(todos, many=True)
        return Response(serializer.data)

    def post(self, request):
        mutable_data = request.data.copy()
        mutable_data['user'] = request.user.pk
        serializer = ToDoSerializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ToDoDetailAPIView(APIView):
    """
        API endpoint for retrieving, updating, and deleting todo items.

        Accepted Request Methods:
        - GET
        - PUT
        - DELETE

        Expected Inputs for PUT:
        - todo_name (string): Name of the todo item.
        - description (string): Description of the todo item.

        GET:
        Get the details of todo item.

        PUT:
        Update the details of todo item.

        DELETE:
        Delete todo item.

        JSON Response for GET and PUT:
        {
            "id": 1,
            "todo_name": "Name",
            "description": "Description of item",
            "status": false,
            "user": 1
        }
    """
    def get_object(self, name):
        try:
            return ToDo.objects.get(user=self.request.user, todo_name=name)
        except ToDo.DoesNotExist:
            raise Http404

    def delete(self, request, name):
        todo_item = self.get_object(name)
        todo_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, name):
        todo_item = self.get_object(name)
        serializer = ToDoSerializer(todo_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
