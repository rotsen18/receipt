from collections import defaultdict

from rest_framework import serializers

from culinary.api.v1.serializers.receipt import ReceiptDetailSerializer
from culinary.models import ReceiptComment, ReceiptSource
from directory.api.v1.serializers.food import CulinaryCategorySerializer
from directory.models import CulinaryCategory


class BotReceiptCommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField(read_only=True)
    date = serializers.DateTimeField(source='created_at', read_only=True, format='%d %b %Y')
    rate = serializers.SerializerMethodField()

    class Meta:
        model = ReceiptComment
        fields = ('text', 'date', 'author', 'rate')

    def get_rate(self, obj):
        return '⭐' * obj.rate

    def get_author(self, obj):
        if obj.author and not obj.author.is_anonymous:
            return obj.author.get_short_name()
        if obj.telegram_user:
            return obj.telegram_user.get_short_name()
        return 'Анонім'


class BotCulinaryCategorySerializer(CulinaryCategorySerializer):
    receipt_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = CulinaryCategory
        fields = ('name', 'id', 'receipt_count')


class ReceiptSourceSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(source='created_at', read_only=True, format='%d %b %Y')

    class Meta:
        model = ReceiptSource
        fields = ('source', 'receipt', 'date')


class BotDetailReceiptSerializer(ReceiptDetailSerializer):
    components = serializers.SerializerMethodField()

    def get_components(self, obj):
        result = defaultdict(list)
        for component in obj.components.all():
            key = 'Складники'
            if component.receipt_components_type:
                key = component.receipt_components_type.name
            result[key].append(str(component))
        return result
