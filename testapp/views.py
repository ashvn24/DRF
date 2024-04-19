from django.shortcuts import render
from rest_framework import generics, status, views
from .models import *
from .serializers import *
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from django.contrib.auth import authenticate,login
from rest_framework.authtoken.models import Token
# Create your views here.

class CreateUserAPIView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer
    
    def create(self, request, *args, **kwargs):
        response =  super().create(request, *args, **kwargs)
        
        return Response(response.data, status=status.HTTP_201_CREATED)
    
class LoginUserAPIView(generics.CreateAPIView):
    serializer_class =LoginSerializer

        
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email=serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
            
class ListUserPIView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class= UserSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes =[IsAuthenticated]
    
    

class TokenLogin(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data= request.data)
        if serializer.is_valid(raise_exception=True):
            email=serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                token, created = Token.objects.get_or_create(user = user)
                return Response({'token':token.key})
            else:
                return Response({'error': 'Invalid credentials'}, status=401)