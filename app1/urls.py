
from django.urls import path,include
from rest_framework.routers import DefaultRouter
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

from .views import *
router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('cart', CartViewSet)

urlpatterns = [
    path('sing/', register, name='sing up'),
    path('login/', login, name='login'),
    # path('home/', product_list_view, name='product-list'),
    path('request-reset-password/', request_reset_password, name='request-reset-password'),
    path('reset-password/<uidb64>/<token>/', reset_password, name='reset-password'),
    # path('products/<int:pk>/', product_detail, name='product-detail'),
    # path('cart/add/', add_to_cart, name='add-to-cart'),
    # path('cart/user/<int:user_id>/', user_cart, name='user-cart'),
    # path('cart/delete/<int:cart_item_id>/', delete_cart_item, name='delete-cart-item'),
    path('api/', include(router.urls)),

]




