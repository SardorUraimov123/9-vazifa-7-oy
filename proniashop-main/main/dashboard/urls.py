from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    
   path('', views.index, name='index'),
    path('category/', views.category_list, name='category_list'),
    path('category/create/', views.category_create, name='category_create'),
    path('category/update/<str:code>/', views.category_update, name='category_update'),
    path('category/delete/<str:code>/', views.category_delete, name='category_delete'),
    path('product/', views.product_list, name='product_list'),
    path('product/detail/<str:code>/', views.product_detail, name='product_detail'),
    path('product/create/', views.product_create, name='product_create'),
    path('product/update/<str:code>/', views.product_update, name='product_update'),
    path('product/delete/<str:code>/', views.product_delete, name='product_delete'),
    path('product/img/delete/<int:id>/', views.product_img_delete, name='product_img_delete'),
    path('product/video/delete/<int:id>/', views.product_video_delete, name='product_video_delete'),
    path('create-product-enter/', views.create_product_enter, name='create_product_enter'),
    path('update-product-enter/<str:code>/', views.update_product_enter, name='update_product_enter'),
    path('list-product-enter/', views.list_product_enter, name='list_product_enter'),
    path('detail-product-enter/<str:code>/', views.detail_product_enter, name='detail_product_enter'),
    path('product-history/<str:code>/', views.product_history, name='product_history'),
    path('page1/chart/', views.page1_chart, name='page1_chart'),
    path('page2/chart/', views.page2_chart, name='page2_chart'),
]