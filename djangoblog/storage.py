from compressor.storage import CompressorFileStorage
from django.core.files.storage import storages
from storages.backends.gcloud import GoogleCloudStorage


class GCSCompressorFileStorage(CompressorFileStorage, GoogleCloudStorage):
    pass


class CachedStorage(GoogleCloudStorage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.local_storage = storages.create_storage(
            {"BACKEND": "compressor.storage.CompressorFileStorage"}
        )

    def save(self, name, content):
        self.local_storage.save(name, content)
        super().save(name, self.local_storage._open(name))
        return name
