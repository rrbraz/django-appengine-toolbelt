import cloudstorage
import mimetypes
import urllib
from django.conf import settings
from django.core.files.storage import Storage
from django.core.files.base import File
from django.utils.encoding import force_unicode

DEFAULT_CONTENT_TYPE = 'application/binary'


class GoogleCloudStorage(Storage):

    def __init__(self, bucket=None):
        self.bucket = bucket or settings.DEFAULT_STORAGE_BUCKET

    def _add_bucket(self, name):
        safe_name = urllib.quote(name.encode('utf-8'))
        return '/{0}/{1}'.format(self.bucket, safe_name)

    def _open(self, name, mode='r'):
        # Handle 'rb' as 'r'.
        mode = mode[:1]
        fp = cloudstorage.open(self._add_bucket(name), mode=mode)
        return File(fp)

    def _content_type_for_name(self, name):
        # guess_type returns (None, encoding) if it can't guess.
        return mimetypes.guess_type(name)[0] or DEFAULT_CONTENT_TYPE

    def _save(self, name, content):
        name = self.get_valid_name(name)  # Make sure the name is valid

        kwargs = {
            'content_type': self._content_type_for_name(name),
        }
        with cloudstorage.open(self._add_bucket(name), 'w', **kwargs) as fp:
            fp.write(content.read())
        return name

    def delete(self, name):
        assert name, "The name argument is not allowed to be empty."
        cloudstorage.delete(self._add_bucket(name))

    def exists(self, name):
        try:
            cloudstorage.stat(self._add_bucket(name))
        except cloudstorage.NotFoundError as e:
            return False
        else:
            return True

    def size(self, name):
        return cloudstorage.stat(self._add_bucket(name)).st_size

    def url(self, name):
        return settings.MEDIA_URL + name

    def get_valid_name(self, name):
        return force_unicode(name).strip().replace('\\', '/')
