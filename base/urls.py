from django.urls import path
from . import views
from . views import *
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
# products #

    path('api/', views.getRoutes, name='routes'),
    path('api/products/', views.getProducts, name='products'),
    path('api/products/sell/<str:pk>', views.sellProduct, name='products'),
    path('api/products/create', views.createProduct, name='create_product'),
    path('api/products/<str:pk>', views.getProduct, name='product'),
    path('api/products/update/<str:pk>/', views.editProduct, name="product-edit"),
    path('api/products/delete/<str:pk>/', views.deleteProduct, name="product-delete"),
    path('api/product/owner/', views.Product_user, name="product_user"),
    path('api/product/owner/<str:pk>/', views.Product_spec, name="product_spec"),
    path('api/products/<str:pk>/bidding', set_bidding, name='set_bidding'),

# orders #

    path('api/orders/', views.getOrders, name='orders'),
    path('api/orders/delete/<str:pk>', views.deleteOrder, name='delete_order'),
    path('api/orders/add', views.addOrderItems, name='create_order'),
    path('api/orders/myorders/',views.getMyOrders,name="myorders"),
    path('api/orders/<str:pk>/',views.getOrderById,name="user-order"),
    path('api/orders/<str:pk>/pay/',views.updateOrderToPaid,name="user-order"),



]