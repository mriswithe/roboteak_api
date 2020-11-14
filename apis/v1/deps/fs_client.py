from google.cloud.firestore import Client


_COMMON_CLIENT = None
if _COMMON_CLIENT is None:
    _COMMON_CLIENT = Client()
