# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

class CralwerPipeline(object):
    def process_item(self, item, spider):
        pass
        item.save()
        # print(item)
        # # 项目信息
        # if "project" in item:
        #     new_house = NewHouse.objects.filter(name=item['project']['name'])
        #     if len(new_house) > 0:
        #         pass
        #     else:
        #         item['project'].save()
        # # 楼栋信息
        # if "building" in item:
        #     house_building = HouseBuilding.objects.filter(name=item['building']['name'],
        #                                                   room_id=item['building']['room_id'])
        #     if len(house_building) > 0:
        #         pass
        #     else:
        #         item['building'].save()
        #
        # # 户型信息
        # if "type" in item:
        #     house_type = HouseType.objects.filter(name=item['type']['name'], house_type=item['type']['house_type'])
        #     if len(house_type) > 0:
        #         pass
        #     else:
        #         item['type'].save()
