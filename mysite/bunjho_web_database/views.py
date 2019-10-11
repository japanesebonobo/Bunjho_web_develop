from django.db.models import Q
from django.shortcuts import render
from .models import Allsubjectdata
from .forms import SearchFormSet
from .models import User

# Create your views here.
def index_page(request):
    data = Allsubjectdata.objects.all().values('subjectname','teacher','units','member','a','b','c','d','f','averagegpa','link').distinct().order_by('subjectno')
    formset = SearchFormSet(request.POST or None)
    if request.method == 'POST':
        formset.is_valid()
        queries = []

        for form in formset:
            q_kwargs = {}
            faculty = form.cleaned_data.get('faculty')
            if faculty:
                q_kwargs['faculty'] = faculty
            genre = form.cleaned_data.get('genre')
            if genre:
                q_kwargs['genre'] = genre
            if q_kwargs:
                q = Q(**q_kwargs)
                queries.append(q)
        if queries:
            # filter(Q(...) | Q(...) | Q(...))を動的に行っている。
            base_query = queries.pop()
            for query in queries:
                base_query &= query
            data = data.filter(base_query)


    params = {
        'title': 'Bunjho_2018_AllSubjectData',
        'message': '2019/10/7',
        'data': data,
        'formset': formset,
    }
    return render(request, 'index.html', params)