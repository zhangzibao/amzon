import sys
import os
import django

sys.path.append('../../../amazon')
os.environ['DJANGO_SETTINGS_MODULE'] = 'amazon.settings'
django.setup()