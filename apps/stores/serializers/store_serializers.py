from rest_framework import serializers
from apps.stores.models import Store
from apps.branches.serializers import BranchOutSerializer


# from apps.branches.serializers import StoreSerializer
class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        exclude = ["created_at", "modified_at", "deleted_at", "is_active"]


class StoreOutSerializer(serializers.ModelSerializer):
    branch = BranchOutSerializer()

    class Meta:
        model = Store
        exclude = ["created_at", "modified_at", "deleted_at", "is_active"]
