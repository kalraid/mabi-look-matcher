"""Phase 0: offline Catalog Merge CLI."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from look_matcher.catalog_merge import CatalogMerge, load_merge_rules
from look_matcher.config import get_settings


def _snapshot_to_dict(snapshot) -> dict:
    return {
        "version": snapshot.version,
        "items": [
            {
                "id": i.id,
                "display_name_ko": i.display_name_ko,
                "slot_ids": i.slot_ids,
                "equip_id": i.equip_id,
                "category": i.category,
                "description": i.description,
                "class_id": i.class_id,
                "internal_name": i.internal_name,
                "thumbnail_url": i.thumbnail_url,
                "dyeable": i.dyeable,
                "server_ids": i.server_ids,
            }
            for i in snapshot.items
        ],
    }


def main(argv: list[str] | None = None) -> int:
    settings = get_settings()
    parser = argparse.ArgumentParser(description="Merge Catalog Sources into a snapshot JSON")
    parser.add_argument(
        "--rules",
        type=Path,
        default=settings.resolve_path(settings.catalog_merge.config_path),
    )
    parser.add_argument(
        "--labanyu",
        type=Path,
        default=settings.resolve_path("tests/fixtures/sources/labanyu/items.json"),
    )
    parser.add_argument(
        "--sigkill",
        type=Path,
        default=settings.resolve_path("tests/fixtures/sources/sigkill/items.json"),
    )
    parser.add_argument(
        "--dump",
        type=Path,
        default=settings.resolve_path(
            "tests/fixtures/sources/community_dump/items.min.json"
        ),
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=settings.resolve_path(settings.catalog.snapshot_path),
    )
    parser.add_argument(
        "--review-queue",
        type=Path,
        default=settings.resolve_path(settings.catalog_merge.review_queue_path),
    )
    args = parser.parse_args(argv)

    merger = CatalogMerge(load_merge_rules(args.rules))
    snapshot = merger.merge(
        labanyu_path=args.labanyu,
        sigkill_path=args.sigkill,
        dump_path=args.dump,
        review_queue_path=args.review_queue,
    )

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as f:
        json.dump(_snapshot_to_dict(snapshot), f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(snapshot.items)} items to {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
