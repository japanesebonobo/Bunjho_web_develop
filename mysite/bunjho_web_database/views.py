from django.shortcuts import render
from .models import Allsubjectdata

# Create your views here.
def index_page(request):
    data = Allsubjectdata.objects.all().values('subjectname','teacher','units','member','a','b','c','d','f','averagegpa','link').distinct().order_by('subjectno')
    params = {
        'title': 'Bunjho_2018_AllSubjectData',
        'message': '2019/10/7',
        'data': data,
    }
    return render(request, 'index.html', params)
