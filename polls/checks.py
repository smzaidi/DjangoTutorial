import datetime
from django.utils import timezone
from watchman.decorators import check
from .models import Choice

@check
def recentActivity():
	recent = timezone.now() - datetime.timedelta(minutes=5)
	if Choice.objects.filter(timestamp__gte=recent).exists():
		return {'recentActivity': True}
	return {'recentActivity': False}
