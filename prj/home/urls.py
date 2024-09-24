from django.urls import path
from . import views

app_name = 'home'
urlpatterns =[
    path('', views.HomeView.as_view(), name='home'),
    path('post/<int:post_id>/<slug:post_slug>', views.PostDetailView.as_view(), name='post'),
    path('post/delete/<int:post_id>', views.DeletePostView.as_view(), name='post-delete'),
    path('post/update/<int:post_id>', views.UpdatePostView.as_view(), name='post-update')
]