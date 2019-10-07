from django.shortcuts import render
from .models import Allsubjectdata

# Create your views here.
def index(request):
    data = Allsubjectdata.objects.all()
    params = {
        'title': 'Bunjho_2018_AllSubjectData',
        'message': '2019/10/7',
        'data': data,
    }
    return render(request, '2018_subject_data/index.html', params)