from rest_framework import serializers
from main.serializers import ProductDetailsSerializer
from main.models import Cart, Product, CartProduct


# создаем сериализатор orderproduct
class CartProductSerializer(serializers.ModelSerializer):
    # product = serializers.CharField(max_length=255)
    # count = serializers.IntegerField()
    class Meta:
        model = CartProduct
        fields = ('product', 'count')


class CartProductRepresentationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='product.id')
    title = serializers.CharField(source='product.title')

    class Meta:
        model = CartProduct
        fields = ('id', 'title', 'price', 'count')


class AddProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id')


class CartSerializer(serializers.ModelSerializer):
    items = CartProductSerializer(many=True, write_only=True)
    class Meta:
        model = Cart
        fields = ('count', 'items')

    def get_total_cost(self, obj):
        return obj.get_total_cost()


    def create(self, validated_data):
        request = self.context.get('request')
        print(request)
        items = validated_data.pop('items')
        print(items)
        cart = Cart.objects.create(**validated_data)
        if request.user.is_authenticated:
            cart.user = request.user
            cart.save()

        for item in items:
            product = item['product']
            # print(product)
            # product_id = request.POST.get('product')
            CartProduct.objects.create(cart=cart, product=product, count=item['count'])
            product.save()
            # product.clean()
        return cart

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.email
        representation['product'] = CartProductRepresentationSerializer(instance.cart.all(), many=True, context=self.context).data
        return representation
