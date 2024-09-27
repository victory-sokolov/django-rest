import json
from typing import Any

from compressor.storage import CompressorFileStorage
from django.core.files.storage import storages
from storages.backends.gcloud import GoogleCloudStorage


class CustomOfflineManifestStorage(CompressorFileStorage):
    """CustomOfflineManifestStorage."""

    def read_manifest(self) -> dict:
        """ "Read manifest file."""
        try:
            with self.open(self.manifest_name) as manifest_file:
                return json.load(manifest_file)
        except OSError:
            return {}


class CachedGCloudStorage(GoogleCloudStorage):
    """Google Cloud storage backend that saves the files locally, too."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.local_storage = storages.create_storage(
            {"BACKEND": "compressor.storage.CompressorFileStorage"},
        )

    def save(self, name: str, content: str) -> str:
        """Save data to local storage."""
        self.local_storage._save(name, content)
        super().save(name, self.local_storage._open(name))
        return name
