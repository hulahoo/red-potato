from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters, viewsets
from main.models import Product, Comment
from .serializers import ProductDetailsSerializer, CommentSerializer
from .permissions import ProductPermission, IsCommentAuthor, IsProductAuthor


class ProductViewSet(ModelViewSet):
    """4ий.Универсальный вариант для всего CRUD в одном классе"""
    queryset = Product.objects.all()
    serializer_class = ProductDetailsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'title', 'price']


    def get_permissions(self):
        """Сюда прилетает какое то действие и если оно равно чтению то ничего не происходит, а если дургое то идет по условию"""
        if self.action in ['list', 'retrieve']:
            permissions = []
        else:
            permissions = [ProductPermission, IsProductAuthor, ]
        return [permission() for permission in permissions]


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [ProductPermission, ]
    queryset = Comment.objects.all()

    def get_permissions(self):
        """Сюда прилетает какое то действие и если оно равно чтению то ничего не происходит, а если дургое то идет по условию"""
        if self.action in ['list', 'retrieve']:
            permissions = []
        else:
            permissions = [IsCommentAuthor, ]
        return [permission() for permission in permissions]


class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])