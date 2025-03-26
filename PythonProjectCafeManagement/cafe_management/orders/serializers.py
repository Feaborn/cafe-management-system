from rest_framework import serializers
from .models import Order, Dish


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['id', 'name', 'price']


class OrderSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'table_number', 'dishes', 'total_price', 'status']
        extra_kwargs = {
            'table_number': {'required': True},
            'status': {'required': True}
        }