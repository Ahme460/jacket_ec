from rest_framework import generics, permissions, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import SingUpSerializer
from .serializers import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from rest_framework.viewsets import ModelViewSet

import os
import importlib
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .tasks import *
import time
from .models import *
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

User = get_user_model()


@api_view(['POST'])
def register(request):
    data = request.data
    serializer = SingUpSerializer(data=data)
    if serializer.is_valid():
        if not User.objects.filter(username=data['username']).exists():
            user = User.objects.create(
                first_name=data['first_name'],
                email=data['email'],
                username=data['username'],
                password=make_password(data['password']),
            )
            # استدعاء مهمة إرسال البريد الإلكتروني
            send_welcome_email.delay(user.email)
            return Response(
                {'details': 'Your account registered successfully!'},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {'error': 'This email already exists!'},
                status=status.HTTP_400_BAD_REQUEST
            )
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    refresh = RefreshToken.for_user(user)
    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })


# @api_view(['GET'])
# def product_list_view(request):
#     products = Products.objects.all()
#     if "color" in request.query_params:
#         colors = request.query_params['color']
#         products = products.filter(color__color__in=colors)
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def request_reset_password(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
        send_reset_password_email.delay(user.email)
        return Response({'details': 'Password reset email sent!'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User with this email does not exist'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def reset_password(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        new_password = request.data.get('password')
        if new_password:
            user.password = make_password(new_password)
            user.save()
            return Response({'details': 'Password has been reset successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Invalid reset link'}, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET'])
# def product_detail(request, pk):
#     try:
#         product = Products.objects.get(pk=pk)
#     except Products.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     serializer = ProductSerializer_detal(product)
#     return Response(serializer.data)


class CartViewSet(ModelViewSet):
    queryset = CartModel.objects.all()
    serializer_class = CartSer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return CartItemSerializer
        return CartSer

    def get_queryset(self):
        return CartModel.objects.filter(customer=self.request.user)


@api_view(['GET'])
def user_cart(request, user_id):
    cart_items = CartItem.objects.filter(user=user_id)

    total_price = 0
    for item in cart_items:
        total_price += item.product.price * item.quantity
    serializer = CartItemSerializer(cart_items, many=True)
    data = serializer.data
    for i in range(len(data)):
        data[i]['total_price'] = cart_items[i].product.price * cart_items[i].quantity
    return Response(data)


@api_view(['DELETE'])
def delete_cart_item(request, cart_item_id):
    try:
        cart_item = CartItem.objects.get(pk=cart_item_id)
    except CartItem.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    cart_item.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class ProductViewSet(ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['color__color', 'sizes__size']
    search_fields = ['name', 'details']
    ordering_fields = ['price', 'id']
