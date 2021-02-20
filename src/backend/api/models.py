from django.db import models

class Report(models.Model):
	username = models.CharField(max_length=100)
	report_name = models.CharField(max_length=200)
	scan_date = models.DateField()
	plugin_check_count = models.IntegerField(default=0)
	severity_level_warning_count = models.IntegerField(default=0)
	severity_level_minor_count = models.IntegerField(default=0)
	severity_level_major_count = models.IntegerField(default=0)
	severity_level_critical_count = models.IntegerField(default=0)
	
	def __str__(self):
		return self.report_name
    
class ItemsFound(models.Model):
	severity = models.CharField(max_length=2)
	plugin_id = models.CharField(max_length=10)
	plugin_name = models.CharField(max_length=200)
	plugin_family = models.CharField(max_length=200)
	description = models.CharField(max_length=1000)
	action = models.CharField(max_length=1000)
	report = models.ForeignKey(Report,related_name='items_found', on_delete=models.CASCADE)

	def __str__(self):
		return self.plugin_name

