# accounts/views/profileView.py
import json

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers.profileSerializer import ProfileSerializer
from redis_client import redis_client

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cached_data = self.get_user_cache(request.user.account_id)
        if cached_data:
            return Response(cached_data)  # serve from Redis

        serializer = ProfileSerializer(request.user)
        self.set_user_cache(request.user)  # store in Redis
        print("wasn't cached")
        return Response(serializer.data)

    def put(self, request):
        serializer = ProfileSerializer(instance=request.user, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            self.set_user_cache(request.user)  # update Redis after DB save
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        serializer = ProfileSerializer(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            self.set_user_cache(request.user)  # update Redis
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_user_cache(account_id):
        key = account_id
        value = redis_client.get(key)
        return json.loads(value) if value else None

    @staticmethod
    def set_user_cache(user):
        key = user.account_id
        data = {
            "account_id": user.account_id,
            "name": user.name,
            "lastname": user.lastname,
            "email": user.email,
            "phone_number": user.phone_number,
            "role": user.role,
            "status": user.status,
        }
        redis_client.setex(key, 60 * 60 * 6, json.dumps(data))  # 6 hours

    @staticmethod
    def delete_user_cache(account_id):
        key = account_id
        redis_client.delete(key)