from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..serializers.profileSerializer import ProfileSerializer


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = {
            "email": user.email,
            "phone_number": user.phone_number,
            "name": user.name,
            "lastname": user.lastname,
            "birth_date": user.birth_date,
            "city": user.city_id if user.city else None,
        }
        return Response(data)

    def put(self, request):
        return self._update(request, partial=False)

    def patch(self, request):
        return self._update(request, partial=True)

    def _update(self, request, partial):
        serializer = ProfileSerializer(instance=request.user, data=request.data, partial=partial, context={"request": request})
        if serializer.is_valid():
            updated = serializer.save()
            return Response(updated)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
