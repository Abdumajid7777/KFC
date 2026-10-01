from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user_username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Review
        fields = ['id', 'user', 'user_username', 'food', 'text', 'rating', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']