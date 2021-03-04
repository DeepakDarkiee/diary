from django.db import models
from django.contrib.auth.models import User

STATUS = ((0, "Draft"), (1, "Publish"))
class Category(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200,null=True)
    slug = models.SlugField(max_length=200,null=True)
            
        
    def __str__(self):
        return self.name


class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="blog_posts")

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True ,null=True)
    # author = models.ForeignKey(
    #     User, on_delete=models.CASCADE, related_name="blog_posts"
    # )
    category = models.ForeignKey('Category',on_delete=models.CASCADE, null=True, blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    productivity = models.IntegerField()


    def date_for_chart(self):
         return self.created_on.strftime('%b %e')

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("post_detail", kwargs={"slug": str(self.slug)})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return "Comment {} by {}".format(self.body, self.name)

class Contact(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField()
    Content = models.TextField(null=True)
    phone= models.CharField(max_length=13,null=True)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_on"]

    def __str__(self):
        return "Contact {} by {}".format(self.body, self.name)

    

# class DiaryModel(models.Model):
#     user=models.ForeignKey(User,on_delete=models.CASCADE)
#     note = models.CharField(max_length=100)
#     content = models.TextField()
#     posted_date = models.DateTimeField()
#     productivity = models.IntegerField()

#     def date_for_chart(self):
#         return self.posted_date.strftime('%b %e')

#     def __str__(self):
#         return self.note

#     def summary(self):
#         if len(self.content) > 100:
#             return self.content[:100] + '  ...'
#         return self.content[:100]
