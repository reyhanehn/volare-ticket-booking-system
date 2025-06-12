# accounts/views/profileView.py
import json

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers.profileSerializer import ProfileSerializer
from cache_utils import get_user_cache, set_user_cache


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cached_data = get_user_cache(request.user.account_id)
        if cached_data:
            return Response(cached_data)  # serve from Redis

        serializer = ProfileSerializer(request.user)
        set_user_cache(request.user)  # store in Redis
        print("wasn't cached")
        return Response(serializer.data)

    def put(self, request):
        serializer = ProfileSerializer(instance=request.user, data=request.data, partial=False)
        if serializer.is_valid():
            result = serializer.save()
            set_user_cache(request.user)  # update Redis
            return Response(result)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        serializer = ProfileSerializer(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            result = serializer.save()
            set_user_cache(request.user)  # update Redis
            return Response(result)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

