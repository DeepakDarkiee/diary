from django.views import generic
from entry.models import Post,Contact
from .forms import CommentForm
from django.shortcuts import render, get_object_or_404,redirect
from django.db.models import Q
from django.views.generic import TemplateView, ListView
from django.contrib import messages
from django.core.mail import send_mail

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by("-created_on")
    template_name = "index.html"
    paginate_by = 3


class SearchResultsView(ListView):
    model = Post
    template_name = 'search_results.html'
    
    def get_queryset(self):
        query = self.request.GET.get('q') # new
        object_list = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) 
        )
        return object_list


# class PostDetail(generic.DetailView):
#     model = Post
#     template_name = 'post_detail.html'


def post_detail(request, id):
    template_name = "post_detail.html"
    post = get_object_or_404(Post, id=id)
    comments = post.comments.filter(active=True).order_by("-created_on")
    new_comment = None
    # Comment posted
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(
        request,
        template_name,
        {
            "post": post,
            "comments": comments,
            "new_comment": new_comment,
            "comment_form": comment_form,
        },
    )


def contact(request):
    if request.method=="POST":
        name =request.POST['name']
        email =request.POST['email']
        phone =request.POST['phone']
        msg=request.POST['content']
        print(name,email,phone,msg)
        if len(name)<2 or len(email)<2 or len(phone)<10 or len(msg)<4:
            messages.error(request,'Please Fill The Form Correctly!',extra_tags='alert')
        else:
            contact = Contact(name=name,email=email,phone=phone,Content=msg)
            contact.save()
            messages.success(request,'Contact Submitted Successfully!',extra_tags='alert')
    
    return render(request,'contact.html')

# def Contact(request):
#     if request.method == 'POST':
#         form = ContactForm(data=request.POST)
#         if form.is_valid():
#             # send email code goes here
#             sender_name = form.cleaned_data['name']
#             sender_email = form.cleaned_data['email']

#             message = "{0} has sent you a new message:\n\n{1}".format(sender_name, form.cleaned_data['body'])
#             send_mail('New Enquiry', message, sender_email, ['themindzworld@gmail.com'])
#             form.save()
            
            
        
#         else:
#             messages.error(request,'Please Fill The Form Correctly!')
            
#     else:
#         form = ContactForm()
#     return render(request, 'contact.html', {'form': form})