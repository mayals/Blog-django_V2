from django.urls import path
from .import views

#  to add feeds for blog posts
from .feeds import LatestPostsFeed
from .views import PostCreateView, PostUpdateView, PostDeleteView


app_name='blog'

urlpatterns = [
    # posts_list
    path('posts/', views.posts_view, name='posts'),   # -- home page
    path('posts_tag/<slug:tag_slug>/', views.posts_view, name='posts-by-tag'), #by tag_slug

    path('post_detail/<int:post_id>', views.post_detail, name='post-detail'),
    path('post_update/<slug:pk>/', PostUpdateView.as_view(), name='post-update'),
    path('post_delete/<slug:pk>/', PostDeleteView.as_view(), name='post-delete'),
    path('post_share/<int:post_id>', views.post_share_email, name='post-share'),

    path('post_create/', PostCreateView.as_view(), name='post-create'),


    # add feeds path
    path('feed/', LatestPostsFeed(), name='post-feed'),

    # add search path
    path('advanced_search/', views.advanced_search, name='advanced-search'),
    path('search_results/', views.search_results, name='search-results'),
]