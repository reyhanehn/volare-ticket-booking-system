from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from accounts.permissions import IsAdmin
from rest_framework.response import Response
from rest_framework import status

from ..serializers.AdminReportSerializer import SearchReportsSerializer, ViewReportSerializer, AnswerReportSerializer


class AnswerReportView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, report_id):
        data = request.data.copy()
        data['report_id'] = report_id
        serializer = AnswerReportSerializer(data=data, context={"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.validated_data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SearchReportsView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        serializer = SearchReportsSerializer(data=request.query_params)
        if serializer.is_valid():
            data = serializer.get_reports()
            return Response(data)
        return Response(serializer.errors, status=400)


class ViewReportView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request, report_id):
        serializer = ViewReportSerializer(data={"report_id": report_id})
        if serializer.is_valid():
            data = serializer.get_report()
            return Response(data)
        return Response(serializer.errors, status=400)