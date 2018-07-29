import sys
import os

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd + "../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "amazon.settings")

import django

django.setup()

from foods.models import Foods, Kinds, Ratings
from django.contrib.auth import get_user_model

User = get_user_model()

import json

with open("./data/data.json", 'r', encoding='utf-8') as load_f:
    load_f = json.load(load_f)
    # foods
    for good in load_f['goods']:
        # kinds
        seller = User.objects.filter(username="seller")
        r_instance = Kinds()
        if seller:
            r_instance.seller = seller[0]
        r_instance.name = good['name']
        r_instance.type = good['type']
        print(r_instance)
        r_instance.save()

        category_name = good["name"]
        category = Kinds.objects.filter(name=category_name)
        for food in good['foods']:
            _instance = Foods()
            _instance.name = food['name']
            _instance.price = food['price']
            # _instance.oldPrice = food['oldPrice']
            _instance.description = food['description']
            _instance.sellCount = food['sellCount']
            _instance.info = food['info']
            _instance.icon = food['icon']
            _instance.image = food['image']

            if food['rating']:
                _instance.rating = food['rating']
            if category:
                _instance.kinds = category[0]
            _instance.save()

# ratings
# for rating in load_f['ratings']:
#     good = User.objects.filter(username="seller")
#     r_instance = Ratings()
#     r_instance.username = rating['username']
#     r_instance.rateTime = rating['rateTime']
#     r_instance.score = rating['score']
#     # r_instance.rateType = rating['rateType']
#     r_instance.text = rating['text']
#     r_instance.avatar = rating['avatar']
#     r_instance.recommend = ".".join(rating['recommend'])
#     r_instance.save()
