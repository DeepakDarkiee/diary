from django.urls import path
from . import views
from .feeds import LatestPostsFeed, AtomSiteNewsFeed


urlpatterns = [
    path("feed/rss", LatestPostsFeed(), name="post_feed"),
    path("feed/atom", AtomSiteNewsFeed()),
    path("", views.PostList.as_view(), name="home"),
    path("contact/", views.contact, name="contact"),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
    # path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path("detail/<int:id>", views.post_detail, name="post_detail"),
    
]

