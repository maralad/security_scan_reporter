import os
from parse.parse_nexus import ParseNessus
from .models import Report, ItemsFound
from api.serializers import ReportSerializer
from django.forms import model_to_dict
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.http import JsonResponse
import datetime
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)


@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
def login(request):
    if request.method == 'GET':
        raise MethodNotAllowed('GET')

    if request.method == 'POST':
        serializer = AuthTokenSerializer(
            data=request.data,
            context={
                'request': request,
            },
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user': model_to_dict(user)
        })


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def nessus_file(request):

    if request.method == 'POST':
        username = request.user.username
        nes_file = request.FILES['file']
        if not nes_file:
            return Response({'error': 'No file posted, please try again'},
                            status=HTTP_400_BAD_REQUEST)

        fs = FileSystemStorage()
        filename = fs.save(nes_file.name, nes_file)
        uploaded_file_url = fs.url(filename)       
        abs_path_to_nessus_file = os.path.join(settings.BASE_DIR,'media', filename)
        parse_nes = ParseNessus(abs_path_to_nessus_file)
        report_name, check_count, sev_level_dict, report_list = parse_nes.parse_nessus()
        
        report = Report(username=request.user.username,report_name=report_name,
                scan_date=datetime.datetime.now(),plugin_check_count=check_count,
                severity_level_warning_count=sev_level_dict['1'],
                severity_level_minor_count=sev_level_dict['2'],
                severity_level_major_count=sev_level_dict['3'],
                severity_level_critical_count=sev_level_dict['4']
                )
        report.save()

        for item_report in report_list:
            item =ItemsFound(severity=item_report.get('severity'),
                    plugin_id=item_report.get('plugin_id'),
                    plugin_name=item_report.get('plugin_name'),
                    plugin_family=item_report.get('plugin_family'),
                    description=item_report.get('description'),
                    action=item_report.get('action'),
                    report=report)
            item.save()

        report_obj = Report.objects.get(pk=report.id)

        if report_obj is not None:
            serializer = ReportSerializer(report_obj)
            return JsonResponse(serializer.data, safe=True,
            status=HTTP_200_OK)
        else:
            return Response({'error': 'No report found'},
                        status=HTTP_404_NOT_FOUND)

    if request.method == 'GET':
         return Response({
            'bla': 'bla',
        },status=HTTP_200_OK)
