from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ToDo
from .serializers import ToDoSerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

class UserRegistrationAPIView(APIView):
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
    def post(self, request):
        logout(request)
        return Response({'message': "Logout successful"})

class ToDoListCreateAPIView(APIView):
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
