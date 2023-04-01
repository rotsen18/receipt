import humanize

from rest_framework import serializers
from rest_framework.reverse import reverse

from culinary.models import Receipt, ReceiptComponent, ReceiptComment


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = (
            'name', 'name', 'description', 'main_cooking_principe', 'procedure', 'category', 'components',
            'estimate_time'
        )


class ReceiptListSerializer(serializers.ModelSerializer):
    link = serializers.SerializerMethodField()
    main_cooking_principe = serializers.CharField(source='main_cooking_principe.name', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_id = serializers.IntegerField(source='category.id', read_only=True)
    raking = serializers.ReadOnlyField()

    def get_link(self, obj):
        request = self.context.get('request')
        detail_url = reverse('receipt-detail', args=[obj.pk], request=request)
        return detail_url

    class Meta:
        model = Receipt
        fields = (
            'id', 'name', 'description', 'main_cooking_principe', 'category_name', 'category_id', 'link', 'raking'
        )


class ReceiptComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiptComponent
        fields = '__all__'


class ReceiptCommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.get_short_name', read_only=True)

    class Meta:
        model = ReceiptComment
        fields = ('text', 'created_at', 'author', 'rate')
        read_only_fields = ('created_at',)


class ReceiptDetailSerializer(serializers.ModelSerializer):
    components = serializers.StringRelatedField(many=True)
    comments = ReceiptCommentSerializer(many=True)
    category = serializers.CharField(source='category.name', read_only=True)
    devices = serializers.SlugRelatedField(many=True, slug_field='name', read_only=True)
    main_cooking_principe = serializers.SlugRelatedField(slug_field='name', read_only=True)
    author = serializers.CharField(source='author__first_name', read_only=True, default='')
    estimate_time = serializers.SerializerMethodField()

    class Meta:
        model = Receipt
        fields = (
            'id', 'name', 'created_at', 'modified_at', 'author', 'description', 'main_cooking_principe', 'procedure',
            'devices', 'category', 'raking', 'comments', 'components', 'source_link', 'estimate_time'
        )

    def get_estimate_time(self, obj):
        _t = humanize.i18n.activate('uk_UA')
        return '' or humanize.naturaldelta(obj.estimate_time)
