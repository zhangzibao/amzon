from rest_framework import serializers
from spiders.models import amazon_goods


class goodSerializer(serializers.ModelSerializer):
    # 覆盖外键字段
    # ratings = ratingSerializer()
    # nums = serializers.SerializerMethodField()
    class Meta:
        model = amazon_goods
        fields = '__all__'
