# Create your views here.

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, HttpResponse
from django.conf import settings
from nodeshot.models import Link, Interface
from rrdgraphs.models import Graph
import rrdtool
import os

def link(request, link_id):
    try:
        link = Link.objects.only('from_interface', 'to_interface').get(pk=link_id)
    except ObjectDoesNotExist:
        raise Http404

    #TODO: in future handle this two in two try catch blocks ?
    try:
        from_graph = link.from_interface.graph.draw_graph
        to_graph = link.to_interface.graph.draw_graph
    except ObjectDoesNotExist:
        raise Http404


    RRD_DIR = '%s/../rrd/' % os.path.dirname(os.path.realpath(__file__))
    rrd_from = '%s/%s.rrd' % (RRD_DIR, from_interface)
    rrd_from_png = '%s/rrd/%s.png' % (settings.MEDIA_ROOT, from_interface)
    rrd_to = '%s/%s.rrd' % (RRD_DIR, to_interface)
    rrd_to_png = '%s/rrd/%s.png' % (settings.MEDIA_ROOT, to_interface)

    rrdtool.graph(rrd_from_png,
        '--imgformat', 'PNG',
        '--width', '720',
        '--height', '140',
        '--start', '-15d',
        '--end', 'now',
        'DEF:graph_out_pre=%s:out:LAST' % rrd_from)

    rrdtool.graph(rrd_to_png,
        '--imgformat', 'PNG',
        '--width', '720',
        '--height', '140',
        '--start', '-15d',
        '--end', 'now',
        'DEF:graph_out_pre=%s:out:LAST' % rrd_to)
     
    return HttpResponse('<img src="%s" /> <img src="%s">' % (rrd_from_png, rrd_to_png))

