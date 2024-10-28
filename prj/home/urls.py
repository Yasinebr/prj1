from django.urls import path
from . import views

app_name = 'home'
urlpatterns =[
    path('', views.HomeView.as_view(), name='home'),
    path('post/<int:post_id>/<slug:post_slug>', views.PostDetailView.as_view(), name='post'),
    path('post/delete/<int:post_id>', views.DeletePostView.as_view(), name='post-delete'),
    path('post/update/<int:post_id>', views.UpdatePostView.as_view(), name='post-update'),
    path('post/create', views.CreatePostView.as_view(), name='post-create'),
    path('reply/<int:post_id>/<int:comment_id>', views.ReplyPostView.as_view(), name='add_reply'),
    path('like/<int:post_id>', views.LikePostView.as_view(), name='post_like')
]