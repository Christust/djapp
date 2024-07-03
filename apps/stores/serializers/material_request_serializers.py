from rest_framework import serializers
from apps.stores.models import MaterialRequest


# from apps.branches.serializers import MaterialRequestSerializer
class MaterialRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialRequest
        exclude = ["created_at", "modified_at", "deleted_at", "is_active"]


class MaterialRequestOutSerializer(serializers.ModelSerializer):
    item = serializers.StringRelatedField()
    store = serializers.StringRelatedField()
    user = serializers.StringRelatedField()

    class Meta:
        model = MaterialRequest
        exclude = ["created_at", "modified_at", "deleted_at", "is_active"]
