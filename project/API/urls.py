from . import views
from django.urls import path

urlpatterns = [
    path('images/', views.PhotoList.as_view(), name= 'Photo-List'),
    path('images/detail/<int:pk>', views.PhotoDetail.as_view(), name= 'Photo-Detail'),
]