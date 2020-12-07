from rest_framework import serializers
from account.serializers import UserSerializer
from main.models import Category, Product, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')



class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text', 'product')

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author_id'] = request.user
        comment = Comment.objects.create(**validated_data)
        return comment


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['author'] = UserSerializer(instance.author_id).data
        return representation


class CommentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('author_id', 'id', 'text', 'product')



class ProductSerializer(serializers.ModelSerializer):
    """Здесь мы используем как в обычном джанго model и наследуемся от ModelSerializer"""
    class Meta:
        """И можем оттуда переопределять их методы"""
        model = Product
        fields = ('id', 'title', 'price', 'category', 'stock')


class ProductDetailsSerializer(serializers.ModelSerializer):
    """Здесь мы используем как в обычном джанго model и наследуемся от ModelSerializer"""
    class Meta:
        """И можем оттуда переопределять их методы"""
        model = Product
        fields = ('id', 'title', 'description', 'price', 'author_id', 'stock')

    def _get_image_url(self, obj):
        """Мы получаем url первой картинки"""
        request = self.context.get('request')  # это у нас словарь и поэтому нужен метод get
        image_obj = obj.images.first()  # если картинка есть то возвращает обьект
        if image_obj is not None and image_obj.image:  # здесь мы проверяем если есть картинка то он вытаскивает url
            url = image_obj.image.url
            if request is not None:  # если request нам пришел не None
                url = request.build_absolute_uri(url)  # то новое значение url будет абсолютным путем старого url
            return url  # и возвращает путь
        return "No Image"  # а если картинки нету то возвращает пустую строку

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['author_id'] = request.user
        product = Product.objects.create(**validated_data)
        return product


    def to_representation(self, instance):
        """формирует то что будет показываться пользователю он формирует словарь"""
        representation = super().to_representation(instance)  # здесь мы вызываем родительский метод
        representation['category'] = CategorySerializer(instance.category.all(),many=True).data  # здесь мы выводим все категории, many=TRue для большого количества постов
        representation['image'] = self._get_image_url(instance)  # instance это обькет класса который мы прогоняем через serializer в нашем случаем это obj
        if "comment" not in self.fields:
            representation['comments'] = CommentSerializer(instance.comment_set.all(), many=True).data
        # representation['author'] = UserSerializer(instance).data
        return representation
