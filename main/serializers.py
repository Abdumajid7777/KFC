from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import (
    Review,     
    Restaurant,
    Category,
    Food,
    Order,
    OrderItem
)
class ReviewSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = ['id', 'user', 'user_username', 'food', 'text', 'rating', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'password',
        )

        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

        return user


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'id',
            'food',
            'quantity',
            'price',
        ]
        read_only_fields = ['price']

    def create(self, validated_data):
        food = validated_data['food']

        validated_data['price'] = food.price

        return super().create(validated_data)


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'status', 'total_price', 'created_at', 'items']
        read_only_fields = ['status', 'total_price', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user

        if not items_data:
            raise serializers.ValidationError({'items': 'Заказ должен содержать хотя бы один товар.'})

        order = Order.objects.create(user=user)
        total_price = 0

        for item_data in items_data:
            food = item_data['food']
            quantity = item_data['quantity']
            price = food.price

            OrderItem.objects.create(
                order=order,
                food=food,
                quantity=quantity,
                price=price
            )
            total_price += price * quantity

        order.total_price = total_price
        order.save()

        if user.email:
            send_mail(
                subject=f'Заказ №{order.id} муваффақиятли яратилди',
                message=f'Ҳурматли {user.username},\n\nСизнинг #{order.id} рақамли заказингиз қабул қилинди.\nУмумий сумма: {total_price} сўм.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )

        return order