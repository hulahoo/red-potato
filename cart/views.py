from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from cart.permission import IsCartHolder, CartPermission
from cart.serializers import CartSerializer, CartProductRepresentationSerializer, CartProduct, CartProductSerializer, \
    AddProductSerializer
from .models import Cart


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsCartHolder, ]


    def get_permissions(self):
        """Сюда прилетает какое то действие и если оно равно чтению то ничего не происходит, а если дургое то идет по условию"""
        if self.action in ['list', 'retrieve']:
            permissions = []
        else:
            permissions = [IsCartHolder, CartPermission, ]
        return [permission() for permission in permissions]


    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
