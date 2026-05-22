"""CatalogMerge — offline merge from mock sources (public interface)."""

from pathlib import Path

from look_matcher.catalog_merge import CatalogMerge, load_merge_rules


def test_merge_combines_fixture_sources_into_snapshot(repo_root: Path) -> None:
    rules = load_merge_rules(repo_root / "config" / "catalog.merge.yaml")
    merger = CatalogMerge(rules)

    snapshot = merger.merge(
        labanyu_path=repo_root / "tests/fixtures/sources/labanyu/items.json",
        sigkill_path=repo_root / "tests/fixtures/sources/sigkill/items.json",
        dump_path=repo_root / "tests/fixtures/sources/community_dump/items.min.json",
    )

    assert snapshot.version == 1
    assert len(snapshot.items) == 2

    dress = next(i for i in snapshot.items if i.display_name_ko == "서큐버스의 옷")
    assert dress.equip_id == "sk-body-001"
    assert dress.slot_ids == ["body"]
    assert dress.class_id == 64001
    assert dress.dyeable is False
    assert "mabikr1" in dress.server_ids


def test_merge_writes_review_queue_on_duplicate_sigkill_ids(
    tmp_path: Path, repo_root: Path
) -> None:
    rules = load_merge_rules(repo_root / "config" / "catalog.merge.yaml")
    merger = CatalogMerge(rules)

    lab = tmp_path / "lab.json"
    lab.write_text("[]", encoding="utf-8")
    sig = tmp_path / "sig.json"
    sig.write_text(
        "["
        '{"equip_id": "x1", "display_name_ko": "충돌 아이템", "slot_ids": ["body"], '
        '"dyeable": false, "server_ids": ["mabikr1"]},'
        '{"equip_id": "x2", "display_name_ko": "충돌 아이템", "slot_ids": ["body"], '
        '"dyeable": true, "server_ids": ["mabikr1"]}'
        "]",
        encoding="utf-8",
    )
    dump = tmp_path / "dump.json"
    dump.write_text("[]", encoding="utf-8")
    review_path = tmp_path / "review.jsonl"

    merger.merge(
        labanyu_path=lab,
        sigkill_path=sig,
        dump_path=dump,
        review_queue_path=review_path,
    )

    assert review_path.is_file()
    assert "duplicate_sigkill_equip_id" in review_path.read_text(encoding="utf-8")
