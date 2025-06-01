from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..serializers.signupSerializer import AccountSignupSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AccountSignupSerializer(data=request.data)
        if serializer.is_valid():
            account = serializer.save()

            refresh = RefreshToken.for_user(account)

            return Response({
                'message': 'Account created successfully',
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
