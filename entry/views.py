from datetime import datetime

from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AddForm
from .models import  Post

@login_required
def entry(request):
    form = AddForm(request.POST or None)

    if request.method == 'POST':

        if form.is_valid():
            user=request.user
            title = request.POST['title']
            content = request.POST['content']
            productivity = request.POST['productivity']
            status = request.POST['status']
            todays_diary = Post()
            todays_diary.title = title
            
            todays_diary.content = content
            todays_diary.productivity = productivity
            todays_diary.status = status
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
    user = request.user
    diaries = Post.objects.filter(user__pk=user.id).order_by('created_on')
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
    diary = get_object_or_404(Post, pk=diary_id)

    return render(
        request,
        'entry/detail.html',
        {
            'show_highlight': True,
            'title': diary.title,
            'subtitle': diary.created_on,
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
    data = Post.objects.filter(user__pk=user.id).order_by('created_on')[:10]
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
