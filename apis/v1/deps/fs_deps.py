from google.cloud.firestore_v1 import (
    AsyncCollectionReference,
    AsyncDocumentReference,
    DocumentSnapshot,
)

from apis.v1.deps.fs_client import _COMMON_CLIENT


async def fs_get_collection(col_path: str) -> AsyncCollectionReference:
    return _COMMON_CLIENT.collection(col_path)


async def fs_get_doc_snap(doc_path: str) -> DocumentSnapshot:
    return await (await fs_get_doc_ref(doc_path)).get()


async def fs_get_doc_ref(doc_path: str) -> AsyncDocumentReference:
    return _COMMON_CLIENT.document(doc_path)
