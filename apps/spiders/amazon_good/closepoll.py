from scrapy.cmdline import execute
import sys, os
from django.core.management.base import BaseCommand, CommandError


def my_job():
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute(['scrapy', 'crawl', 'amazon_good'])
    # self.stdout.write('Successfully closed poll "%s"' % poll_id)


if __name__ == "__main__":
    my_job()
# import django
# from spiders.tools.proxyip import GetIP
#
# sys.path.append('../../../Charlotte')
# os.environ['DJANGO_SETTINGS_MODULE'] = 'Charlotte.settings'
# django.setup()
#
# getip = GetIP()
# print(getip.get_random_ip())
