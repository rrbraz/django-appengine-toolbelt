import cloudstorage
from django.conf import settings
from django.core.files.storage import Storage
from django.core.files.base import File


class GoogleCloudStorage(Storage):

    def __init__(self, bucket=None):
        self.bucket = bucket or settings.DEFAULT_STORAGE_BUCKET
        self.bucket = '/' + self.bucket + '/'

    def _open(self, name, mode='r'):
        mode = mode[:1]
        return File(cloudstorage.open(self.bucket + name, mode))

    def _save(self, name, content):
        gcs_file = None
        for chunk in content.chunks():
            if gcs_file is None:
                gcs_file = cloudstorage.open(self.bucket + name, 'w')
            gcs_file.write(chunk)
        if gcs_file is not None:
            gcs_file.close()
        return name

    def delete(self, name):
        assert name, "The name argument is not allowed to be empty."
        cloudstorage.delete(self.bucket + name)

    def exists(self, name):
        try:
            cloudstorage.stat(self.bucket + name)
        except cloudstorage.NotFoundError as e:
            return False
        else:
            return True

    def size(self, name):
        return cloudstorage.stat(self.bucket + name).st_size

    def url(self, name):
        return settings.MEDIA_URL + name
