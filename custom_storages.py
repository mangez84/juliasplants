# pylint: disable=W0223
'''Storage of static and media files in an AWS S3 bucket'''

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    '''Location of static files'''
    location = settings.STATICFILES_LOCATION


class MediaStorage(S3Boto3Storage):
    '''Location of media files'''
    location = settings.MEDIAFILES_LOCATION
