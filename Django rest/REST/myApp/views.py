from django.shortcuts import render,redirect
from django.http import request
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializer import UserSerializer
import requests
from django.shortcuts import get_object_or_404
# Create your views here.


@api_view(["GET"])
def get_user(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many = True)
    return Response(serializer.data)
    # return Response(UserSerializer({'name' : 'Azar', 'age' : 23}).data)

@api_view(["POST"])
def create_user(request):
    serializer = UserSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def user_detail(request, pk):
    try:
        user = User.objects.get(pk = pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



def user_interface(request):
    response = requests.get('http://127.0.0.1:8000/api/users/')
    users = response.json()  # Get the user data in JSON format
    return render(request, 'index.html', {'users': users})

@api_view(['GET', 'POST'])
def user_update(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Render a form for the user to update details
        serializer = UserSerializer(user)
        return render(request, 'user_update.html', {'user': serializer.data})

    elif request.method == 'POST':
        # Handle form submission to update user details
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('user_interface')  # Redirect after successful update
        return render(request, 'user_update.html', {'user': serializer.data, 'errors': serializer.errors})

@api_view(['GET', 'DELETE'])
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    # Perform the deletion
    if request.method == 'POST':
        user.delete()
        return redirect('user_interface')  # Redirect after deletion
