from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass(frozen=True)
class MergeRules:
    version: int
    field_precedence: dict[str, list[str]]
    review_queue_path: str


@dataclass(frozen=True)
class CatalogItem:
    id: str
    display_name_ko: str
    slot_ids: list[str]
    equip_id: str | None = None
    category: str | None = None
    description: str | None = None
    class_id: int | None = None
    internal_name: str | None = None
    thumbnail_url: str | None = None
    dyeable: bool | None = None
    server_ids: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class CatalogSnapshot:
    version: int
    items: list[CatalogItem]


def load_merge_rules(path: Path) -> MergeRules:
    with path.open(encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}
    return MergeRules(
        version=int(raw.get("version", 1)),
        field_precedence=dict(raw.get("field_precedence", {})),
        review_queue_path=str(
            raw.get("on_conflict", {}).get("review_queue_path", "data/merge_review.jsonl")
        ),
    )


def _normalize_name(name: str) -> str:
    return re.sub(r"\s+", "", name.strip().lower())


def _load_json_list(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"expected JSON array in {path}")
    return [x for x in data if isinstance(x, dict)]


class CatalogMerge:
    """Merge Catalog Source fixtures/files into a CatalogSnapshot."""

    def __init__(self, rules: MergeRules) -> None:
        self._rules = rules

    def merge(
        self,
        *,
        labanyu_path: Path,
        sigkill_path: Path,
        dump_path: Path,
        review_queue_path: Path | None = None,
    ) -> CatalogSnapshot:
        review_path = review_queue_path or Path(self._rules.review_queue_path)
        review_lines: list[str] = []

        labanyu = {_normalize_name(r["display_name_ko"]): ("labanyu", r) for r in _load_json_list(labanyu_path) if r.get("display_name_ko")}
        sigkill_raw = _load_json_list(sigkill_path)
        sigkill: dict[str, list[tuple[str, dict[str, Any]]]] = {}
        for r in sigkill_raw:
            name = r.get("display_name_ko")
            if not name:
                continue
            key = _normalize_name(name)
            sigkill.setdefault(key, []).append(("sigkill", r))

        for key, rows in sigkill.items():
            equip_ids = {row[1].get("equip_id") for row in rows if row[1].get("equip_id")}
            if len(equip_ids) > 1:
                review_lines.append(
                    json.dumps(
                        {"reason": "duplicate_sigkill_equip_id", "key": key, "equip_ids": sorted(equip_ids)},
                        ensure_ascii=False,
                    )
                )

        dump_by_name = {
            _normalize_name(r["display_name_ko"]): ("community_dump", r)
            for r in _load_json_list(dump_path)
            if r.get("display_name_ko")
        }
        dump_by_class = {
            int(r["class_id"]): ("community_dump", r)
            for r in _load_json_list(dump_path)
            if r.get("class_id") is not None
        }

        all_keys = set(labanyu) | set(sigkill) | set(dump_by_name)
        items: list[CatalogItem] = []

        for key in sorted(all_keys):
            sources: dict[str, dict[str, Any]] = {}
            if key in labanyu:
                sources["labanyu"] = labanyu[key][1]
            if key in sigkill:
                sources["sigkill"] = sigkill[key][0][1]
            if key in dump_by_name:
                sources["community_dump"] = dump_by_name[key][1]

            item = self._build_item(key, sources, dump_by_class)
            if item is not None:
                items.append(item)

        if review_lines:
            review_path.parent.mkdir(parents=True, exist_ok=True)
            with review_path.open("a", encoding="utf-8") as f:
                for line in review_lines:
                    f.write(line + "\n")

        return CatalogSnapshot(version=1, items=items)

    def _pick(self, field: str, sources: dict[str, dict[str, Any]]) -> Any:
        for source_id in self._rules.field_precedence.get(field, []):
            record = sources.get(source_id)
            if not record:
                continue
            mapping = {
                "slot_ids": "slot_ids",
                "equip_id": "equip_id",
                "race_gender_gates": "race_gender_gates",
                "display_name_ko": "display_name_ko",
                "category": "category",
                "description": "description",
                "class_id": "class_id",
                "internal_name": "internal_name",
                "thumbnail_url": "thumbnail_url",
                "dyeable": "dyeable",
                "server_ids": "server_ids",
            }
            attr = mapping.get(field, field)
            if attr in record and record[attr] is not None:
                return record[attr]
        return None

    def _build_item(
        self,
        key: str,
        sources: dict[str, dict[str, Any]],
        dump_by_class: dict[int, tuple[str, dict[str, Any]]],
    ) -> CatalogItem | None:
        display = self._pick("display_name_ko", sources)
        if not display:
            return None

        class_id = self._pick("class_id", sources)
        dump_row = dump_by_class.get(class_id) if class_id is not None else None
        if dump_row and "community_dump" not in sources:
            sources = {**sources, "community_dump": dump_row[1]}

        equip_id = self._pick("equip_id", sources)
        slot_ids = self._pick("slot_ids", sources) or []
        server_ids = self._pick("server_ids", sources) or []

        return CatalogItem(
            id=equip_id or f"name-{_normalize_name(display)}",
            display_name_ko=str(display),
            slot_ids=list(slot_ids),
            equip_id=str(equip_id) if equip_id else None,
            category=self._pick("category", sources),
            description=self._pick("description", sources),
            class_id=int(class_id) if class_id is not None else None,
            internal_name=self._pick("internal_name", sources),
            thumbnail_url=self._pick("thumbnail_url", sources),
            dyeable=self._pick("dyeable", sources),
            server_ids=list(server_ids),
        )
