from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from ..serializers.costumerReportSerializer import ListMyReportsSerializer, CostumerReportSerializer


class CreateReportView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CostumerReportSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            report = serializer.save()
            return Response({
                "message": "Report sent successfully",
                "data": report
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListMyReportsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = ListMyReportsSerializer.get_reports(request.user.account_id)
        return Response(data)

