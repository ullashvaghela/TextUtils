from django.urls import path
from . import views

urlpatterns = [
    path('', views.CategoryList.as_view()),
    path('add/', views.CategoryList.as_view()),
    path('update/<int:pk>/', views.CategoryDetails.as_view()),
    path('delete/<int:pk>/', views.CategoryDetails.as_view()),
    path('search/', views.CategoryList.as_view(),name='categorysearch'),
    #path('category/(?P<name>.+)/$', views.CategorySearch.as_view()),
    path('subcategory/', views.SubcatregoryList.as_view()),
    path('subcategory/add', views.SubcatregoryList.as_view()),
    path('subcategory/update/<int:pk>/', views.SubcatregoryDetails.as_view()),
    path('subcategory/delete/<int:pk>/', views.SubcatregoryDetails.as_view()),    
    path('subcategory/search/', views.SubcatregoryList.as_view(),name='subcategorysearch'), 
]