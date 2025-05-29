
from django.urls import path
from . import views
urlpatterns = [
    path('',views.index, name='dashboard-index'),
    path('product',views.product, name='dashboard-product'),
    path('product/manage',views.product_manage, name='dashboard-product-manage'),
    path('product/update/<int:pk>/',views.product_update, name='dashboard-product-update'),
    path('product/view/<int:pk>/',views.product_view, name='dashboard-product-view'),
    path('order',views.order, name='dashboard-order'),
    path('order/manage',views.order_manage, name='dashboard-order-manage'),
    path('order/update/<int:pk>/',views.order_update, name='dashboard-order-update'),
    path('user',views.user,name='dashboard-user'),
    path('user/manage',views.user_manage, name='dashboard-user-manage'),
    path('user/view/<int:pk>/',views.user_view, name='dashboard-user-view'),
    path('<str:model_name>/delete/<int:pk>/', views.delete, name='dashboard-delete'),
    path('order/history/',views.order_history,name = 'dashboard-order-history'),
    path('product/history/',views.product_history,name = 'dashboard-product-history'),
    #XML
    path('export/products/', views.product_xml, name='export-products'),
    path('export/orders/', views.order_xml, name='export-orders'),
    path('export/order-history/', views.order_history_xml, name='export-order-history'),
    path('export/product-history/', views.product_history_xml, name='export-product-history'),
    path('export/users/', views.user_xml, name='export-users'),

]
