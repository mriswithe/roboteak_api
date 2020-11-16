from google.cloud.firestore_v1 import (
    CollectionReference,
    DocumentReference,
    DocumentSnapshot,
)

from apis.v1.deps.fs_client import _COMMON_CLIENT


async def fs_get_collection(col_path: str) -> CollectionReference:
    return _COMMON_CLIENT.collection(col_path)


async def fs_get_doc_snap(doc_path: str) -> DocumentSnapshot:
    return (await fs_get_doc_ref(doc_path)).get()


async def fs_get_doc_ref(doc_path: str) -> DocumentReference:
    return _COMMON_CLIENT.document(doc_path)
