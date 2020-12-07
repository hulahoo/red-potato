from rest_framework import serializers
from main.models import Product
from .models import Cart, CartProduct


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartProduct
        fields = ('product', 'quantity')



class CartProductRepresentationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='product.id')
    title = serializers.CharField(source='product.title')
    class Meta:
        model = CartProduct
        fields = ('id', 'title', 'price', 'quantity')


class AddProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', )


class CartSerializer(serializers.ModelSerializer):
    items = CartProductSerializer(many=True, write_only=True)
    quantity = serializers.IntegerField(required=False, default=1)
    class Meta:
        model = Cart
        fields = ('id', 'quantity', 'items')

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
            CartProduct.objects.create(cart=cart, product=product, count=item['quantity'])
            product.save()
        return cart


    def update(self, instance, validated_data):
        print('hel')
        instance.quantity = validated_data.get('quantity', instance.count)
        instance.save()
        return instance


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = instance.user.email
        representation['product'] = CartProductRepresentationSerializer(instance.cart.all(), many=True, context=self.context).data
        return representation

