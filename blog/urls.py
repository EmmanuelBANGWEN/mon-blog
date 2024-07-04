from django.urls import path

from . import views
urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('<int:year>/<int:month>/<int:day>/<slug>/', 
         views.post_detail, name='post_detail'),
    path('<int:year>/<int:month>/<int:day>/<slug>/update/', 
         views.post_update, name='post_update'),
    path('category/<slug:category>/', views.post_list, name='category_post_list'),
    path('search/', views.post_search, name='post_search'),
    path('add/', views.add_post, name='add_post'),
    path('<int:post_id>/stream/', views.stream_view, name='stream'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),





    #path('', views.PostListView.as_view(), name = 'post_list'),
]