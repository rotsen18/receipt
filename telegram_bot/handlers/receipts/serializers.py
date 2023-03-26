from rest_framework import serializers

from culinary.models import ReceiptComment
from directory.api.v1.serializers.food import CulinaryCategorySerializer
from directory.models import CulinaryCategory


class BotReceiptCommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.get_short_name', read_only=True, default='Анонім')
    date = serializers.DateTimeField(source='created_at', read_only=True, format='%d %b %Y')
    rate = serializers.SerializerMethodField()

    class Meta:
        model = ReceiptComment
        fields = ('text', 'date', 'author', 'rate')

    def get_rate(self, obj):
        return '⭐' * obj.rate


class BotCulinaryCategorySerializer(CulinaryCategorySerializer):
    receipt_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = CulinaryCategory
        fields = ('name', 'id', 'description', 'receipt_count')
