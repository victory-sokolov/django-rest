from django.contrib.staticfiles.storage import ManifestStaticFilesStorage
from storages.backends.gcloud import GoogleCloudStorage


class GoogleCloudStaticFilesStorage(GoogleCloudStorage, ManifestStaticFilesStorage):
    pass
