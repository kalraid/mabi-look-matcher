"""Uvicorn entry: uvicorn apps.api.main:app"""

from look_matcher.api.app import app

__all__ = ["app"]
