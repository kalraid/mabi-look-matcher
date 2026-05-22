from __future__ import annotations

import time
from dataclasses import dataclass


@dataclass
class _Blob:
    data: bytes
    content_type: str
    expires_at: float


class EphemeralBlobStore:
    """In-memory Ephemeral Upload store; deletes on run complete."""

    def __init__(self, *, ttl_seconds: int = 3600) -> None:
        self._ttl = ttl_seconds
        self._blobs: dict[str, _Blob] = {}

    def put(self, run_id: str, data: bytes, *, content_type: str) -> None:
        self._blobs[run_id] = _Blob(
            data=data,
            content_type=content_type,
            expires_at=time.time() + self._ttl,
        )

    def get(self, run_id: str) -> bytes | None:
        blob = self._blobs.get(run_id)
        if blob is None:
            return None
        if time.time() > blob.expires_at:
            self.delete(run_id)
            return None
        return blob.data

    def delete(self, run_id: str) -> None:
        self._blobs.pop(run_id, None)

    def has(self, run_id: str) -> bool:
        return run_id in self._blobs
