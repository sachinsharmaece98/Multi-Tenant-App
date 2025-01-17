
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.cache import cache

class UserListCreateView(APIView):

    def get(self, request):

        cache_key = "all_users"
        cached_users = cache.get(cache_key)

        if cached_users:
            # Return cached data if available
            return Response(cached_users)

        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        cache.set(cache_key, serializer.data, timeout=3600)
        return Response(serializer.data)
        
    @swagger_auto_schema(
        operation_description="Create a new user",
        request_body=UserSerializer,
        responses={201: UserSerializer, 400: "Bad Request"}
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            cache.delete("all_users")
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
   
    def get_object(self, pk):

        cache_key = f"user_{pk}"
        cached_user = cache.get(cache_key)

        if cached_user:
            # Return cached data if available
            return cached_user
            
        try:
            user = User.objects.get(pk=pk)
            cache.set(cache_key, user, timeout=3600)  # Cache for 1 hour
            return user
        except User.DoesNotExist:
            return None

    def get(self, request, pk):
        user = self.get_object(pk)
        if user:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Update a user by ID",
        request_body=UserSerializer,
        responses={200: UserSerializer, 400: "Bad Request", 404: "Not Found"}
    )
    def put(self, request, pk):
        user = self.get_object(pk)
        if user:
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()

                cache_key = f"user_{pk}"
                cache.set(cache_key, user, timeout=3600)
                cache.delete("all_users")
                
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        user = self.get_object(pk)
        if user:
            user.delete()

            cache_key = f"user_{pk}"
            cache.delete(cache_key)
            cache.delete("all_users")
            
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
