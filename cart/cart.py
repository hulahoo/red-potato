from decimal import Decimal
from django.conf import settings
from main.models import Product


class Cart(object):
    def __init__(self, request):
        """Инициализация обьекта корзины"""
        self.session = request.session  # из запроса мы выхватываем сессию
        cart = self.session.get(settings.CART_SESSION_ID)  # пытаемся получить данные корзины,
        if not cart:  # Если не получаем объект корзины, создаем ее как пустой словарь в сессии.
            # сохраняем сессию в пустую корзину
            cart = self.session[settings.CART_SESSION_ID] = {}  # В этом словаре ключами будут являться ID товаров, а значениями – количество и цена.
        self.cart = cart

    def add(self, product, quantity=1, update_quantity=False):
        """Добавление товара в корзину или обновление его количества."""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:  # update_quantity – булево значение, которое говорит о том, нужно ли заменить значение количества товаров на новое (True) или следует добавить его к существующему (False).
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
     """Помечаем сессию как измененную"""
     self.session.modified = True  # Так мы говорим Django о том, что редактировали данные сессии, а теперь их необходимо сохранить.

    def remove(self, product):  # Метод remove() удаляет товар из корзины и сохраняет новые данные сессии, обращаясь к методу save().
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def __iter__(self):
        """Проходим по товарам корзины и получаем соответствующие объекты Product."""
        product_ids = self.cart.keys()
        # Получаем объекты модели Product и передаем их в корзину.
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
        yield item

    def __len__(self):
        """Возвращает общее количество товаров в корзине."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
        )

    def clear(self):
        # Очистка корзины.
        del self.session[settings.CART_SESSION_ID]
        self.save()