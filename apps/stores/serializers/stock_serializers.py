from rest_framework import serializers
from apps.stores.models import Stock

# from apps.branches.serializers import StockSerializer


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        exclude = ["created_at", "modified_at", "deleted_at", "is_active"]


class StockOutSerializer(serializers.ModelSerializer):
    store = serializers.StringRelatedField()
    item = serializers.StringRelatedField()

    class Meta:
        model = Stock
        exclude = ["created_at", "modified_at", "deleted_at", "is_active"]
