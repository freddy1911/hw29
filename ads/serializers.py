from rest_framework import serializers

from ads.models import Ad, Category
from users.serializers import UserInfoSerializer


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class AdListSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())
    author = UserInfoSerializer()

    class Meta:
        model = Ad
        fields = ['name', 'price', 'author', 'category']


class AdDetailSerializer(serializers.ModelSerializer):
    author = UserInfoSerializer()
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())

    class Meta:
        model = Ad
        fields = '__all__'
