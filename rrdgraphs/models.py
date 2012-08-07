from django.db import models
from nodeshot.models import Interface
# Create your models here.
from django.utils.translation import ugettext_lazy as _

class Graph(models.Model):
	interface = models.OneToOneField(Interface)
	draw_graph = models.BooleanField(_('Draw graphs'), help_text=_('Draw graphs from/to this interface'), default=True)	
