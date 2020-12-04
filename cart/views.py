from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from cart.permission import IsCartHolder
from cart.serializers import CartSerializer
from .models import Cart


class CartViewSet(viewsets.ModelViewSet):
    model = Cart
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated, IsCartHolder, ]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
