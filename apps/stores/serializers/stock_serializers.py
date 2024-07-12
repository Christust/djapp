from rest_framework import serializers
from apps.stores.models import Stock
from apps.stores.serializers.item_serializers import ItemOutSerializer
from apps.stores.serializers.store_serializers import StoreOutSerializer

# from apps.branches.serializers import StockSerializer


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        exclude = ["created_at", "modified_at", "deleted_at", "is_active"]


class StockOutSerializer(serializers.ModelSerializer):
    store = StoreOutSerializer()
    item = ItemOutSerializer()

    class Meta:
        model = Stock
        exclude = ["created_at", "modified_at", "deleted_at", "is_active"]
