
from rest_framework import serializers
from api.models import Report, ItemsFound



class ItemsFoundSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemsFound
        fields = ['severity', 'plugin_id', 'plugin_name', 'plugin_family','description','action']


class ReportSerializer(serializers.ModelSerializer):
    items_found = ItemsFoundSerializer(many=True, read_only=True)

    class Meta:
        model = Report
        fields = ['username', 'report_name', 'scan_date', 'plugin_check_count', 'severity_level_warning_count',
                    'severity_level_minor_count','severity_level_major_count','severity_level_critical_count','items_found']