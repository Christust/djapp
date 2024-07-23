from rest_framework import serializers
from apps.stores.models import StockRequest

# from apps.branches.serializers import StockRequestSerializer

class StockRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockRequest
        exclude = ["created_at", "modified_at", "deleted_at", "is_active"]


class StockRequestOutSerializer(serializers.ModelSerializer):
    stock = serializers.StringRelatedField()
    material_request = serializers.StringRelatedField()

    class Meta:
        model = StockRequest
        exclude = ["created_at", "modified_at", "deleted_at", "is_active"]
