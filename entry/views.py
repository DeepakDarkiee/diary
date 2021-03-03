from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AddForm
from .models import DiaryModel

@login_required
def entry(request):
    form = AddForm(request.POST or None)

    if request.method == 'POST':

        if form.is_valid():
            user=request.user
            note = request.POST['note']
            content = request.POST['content']
            posted_date = datetime.now()
            productivity = request.POST['productivity']

            todays_diary = DiaryModel()
            todays_diary.note = note
            todays_diary.posted_date = posted_date
            todays_diary.content = content
            todays_diary.productivity = productivity
            todays_diary.user=user

            todays_diary.save()

        """
            Clear the form and return.
            3:21 PM 10/19/19 by Arjun Adhikari
        """
        return HttpResponseRedirect('show')

    return render(
        request,
        'entry/add.html',
        {
            'title': 'Write Something',
            'subtitle': 'Add what you feel and we\'ll store it for you.',
            'add_highlight': True,
            'author':request.user.first_name+" "+request.user.last_name,
            'addform': form,
            
        }
    )

@login_required

def show(request):
    """
        We need to show the diaries sorted by date posted in descending order
        5:32 PM 10/19/19 by Arjun Adhikari
    """
    user = request.user
    diaries = DiaryModel.objects.filter(user__pk=user.id).order_by('posted_date')
    diaries_count=diaries.count()
    icon = True if len(diaries) == 0 else None

    return render(
        request,
        'entry/show.html',
        {
            'show_highlight': True,
            'title': 'Total Entries',
            'subtitle': 'It\'s all you\'ve written.',
            'diaries': reversed(diaries),
            'author':request.user.first_name+" "+request.user.last_name,
            'icon': icon,
            'diaries_count':diaries_count
        }
    )

@login_required

def detail(request, diary_id):
    diary = get_object_or_404(DiaryModel, pk=diary_id)

    return render(
        request,
        'entry/detail.html',
        {
            'show_highlight': True,
            'title': diary.note,
            'subtitle': diary.posted_date,
            'author': diary.user.first_name+' '+diary.user.last_name,
            'diary': diary
        }
    )

@login_required

def productivity(request):
    
    """
        At max, draw chart for last 10 data.
        11:24 PM 10/19/19 by Arjun Adhikari
    """
    user = request.user
    data = DiaryModel.objects.filter(user__pk=user.id).order_by('posted_date')[:10]
    icon = True if len(data) == 0 else None

    return render(
        request,
        'entry/productivity.html',
        {
            'title': 'Productivity Chart',
            'subtitle': 'Keep the line heading up always.',
            'data': data,
            'icon': icon,
            'author':request.user.first_name+" "+request.user.last_name,

        }
    )
