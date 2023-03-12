from rest_framework import serializers

from culinary.models import ReceiptComment


class BotReceiptCommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.get_short_name', read_only=True, default='Анонім')
    date = serializers.DateTimeField(source='created_at', read_only=True, format='%d %b %Y')
    rate = serializers.SerializerMethodField()

    class Meta:
        model = ReceiptComment
        fields = ('text', 'date', 'author', 'rate')

    def get_rate(self, obj):
        return '⭐' * obj.rate
