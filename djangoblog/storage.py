from typing import Any, Optional

from django.core.files.storage import storages
from google.cloud.exceptions import NotFound
from google.cloud.storage.retry import DEFAULT_RETRY
from storages.backends.gcloud import GoogleCloudStorage
from storages.utils import clean_name


class CachedGCloudStorage(GoogleCloudStorage):
    """Google Cloud storage backend that saves the files locally, too."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.local_storage = storages.create_storage(
            {"BACKEND": "compressor.storage.DefaultOfflineManifestStorage"},
        )

    def save(self, name: str, content: str) -> str:
        self.local_storage.save(name, content)
        super().save(name, self.local_storage._open(name))
        return name

    def exists(self, name: Optional[str]) -> bool:
        print("Name ->", name)
        if name:
            try:
                self.bucket.delete_blob(name, retry=DEFAULT_RETRY)
            except NotFound:
                pass
        else:
            try:
                self.client.get_bucket(self.bucket)
                return True
            except NotFound:
                return False

        name = self._normalize_name(clean_name(name))
        return bool(self.bucket.get_blob(name))
