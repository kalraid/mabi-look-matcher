"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { useSearchParams } from "next/navigation";
import { getAnalysisRun, startAnalysisRun } from "@/lib/api";
import {
  decodePresetFromUrl,
  encodePreset,
  presetToEquipped,
} from "@/lib/presetCodec";
import type {
  AnalysisRunResponse,
  BaseCharacter,
  Candidate,
  EquippedState,
} from "@/lib/types";

const SLOT_ORDER = [
  "body",
  "robe",
  "wings",
  "head",
  "gloves",
  "shoes",
  "accessory1",
  "wig",
];
const DEPTH_URL =
  process.env.NEXT_PUBLIC_DEPTH_PREVIEW_URL ??
  "https://mabi.sigkill.kr/charsimulator/";
const PRESET_PARAM = process.env.NEXT_PUBLIC_LOOK_PRESET_SHARE_PARAM ?? "preset";

export default function HomeClient() {
  const searchParams = useSearchParams();
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [serverId, setServerId] = useState(
    process.env.NEXT_PUBLIC_DEFAULT_SERVER_ID ?? "mabikr1"
  );
  const [base, setBase] = useState<BaseCharacter>({
    race: "human",
    gender: "female",
    age: 20,
  });
  const [runId, setRunId] = useState<string | null>(null);
  const [analysis, setAnalysis] = useState<AnalysisRunResponse | null>(null);
  const [busy, setBusy] = useState(false);
  const [equipped, setEquipped] = useState<EquippedState>({});
  const [activeTab, setActiveTab] = useState<"flat" | "depth">("flat");
  const [dragPayload, setDragPayload] = useState<{
    slotId: string;
    candidate: Candidate;
  } | null>(null);

  useEffect(() => {
    const token = searchParams.get(PRESET_PARAM);
    const preset = decodePresetFromUrl(token);
    if (!preset) return;
    setServerId(preset.server.server_id);
    setBase(preset.base);
    setEquipped(presetToEquipped(preset));
  }, [searchParams]);

  useEffect(() => {
    if (!runId) return;
    let cancelled = false;
    const poll = async () => {
      const data = await getAnalysisRun(runId);
      if (cancelled) return;
      setAnalysis(data);
      if (data.status === "running") {
        setTimeout(poll, 800);
      }
    };
    poll();
    return () => {
      cancelled = true;
    };
  }, [runId]);

  const onFile = (file: File | null) => {
    setImageFile(file);
    if (imagePreview) URL.revokeObjectURL(imagePreview);
    setImagePreview(file ? URL.createObjectURL(file) : null);
  };

  const startRun = async () => {
    if (!imageFile) return;
    setBusy(true);
    try {
      const id = await startAnalysisRun(imageFile, serverId, base);
      setRunId(id);
      setAnalysis(null);
    } finally {
      setBusy(false);
    }
  };

  const equip = useCallback((slotId: string, c: Candidate) => {
    setEquipped((prev) => ({
      ...prev,
      [slotId]: {
        itemId: c.id,
        dyeable: c.dyeable,
        dyeHint: c.dyeable ? [120, 40, 180] : undefined,
      },
    }));
  }, []);

  const layers = useMemo(() => {
    return SLOT_ORDER.filter((slot) => equipped[slot]).map((slot) => {
      const e = equipped[slot];
      const color = e.dyeOverride ?? e.dyeHint;
      return { slot, itemId: e.itemId, color };
    });
  }, [equipped]);

  const copyShareLink = () => {
    const token = encodePreset(serverId, "kr", base, equipped);
    const url = new URL(window.location.href);
    url.searchParams.set(PRESET_PARAM, token);
    void navigator.clipboard.writeText(url.toString());
    alert("Share Link copied (no reference image included)");
  };

  const onDragStart = (slotId: string, candidate: Candidate) =>
    setDragPayload({ slotId, candidate });
  const onDropPreview = (targetSlot: string) => {
    if (!dragPayload) return;
    equip(targetSlot, dragPayload.candidate);
    setDragPayload(null);
  };

  return (
    <main>
      <section className="panel preview-area">
        <h1>Look Matcher</h1>
        <div>
          <button type="button" onClick={() => setActiveTab("flat")}>
            Flat Preview
          </button>{" "}
          <button type="button" onClick={() => setActiveTab("depth")}>
            Depth Preview <span className="badge">beta</span>
          </button>
        </div>

        {activeTab === "flat" ? (
          <div
            className="layer-stack"
            onDragOver={(e) => e.preventDefault()}
            onDrop={() => onDropPreview("body")}
          >
            {layers.length === 0 && (
              <p>착용한 아이템이 여기 표시됩니다. 후보를 클릭하거나 드래그하세요.</p>
            )}
            {layers.map((layer) => (
              <div
                key={layer.slot}
                className="layer"
                style={{
                  borderLeft: layer.color
                    ? `8px solid rgb(${layer.color.join(",")})`
                    : undefined,
                }}
                onDragOver={(e) => e.preventDefault()}
                onDrop={() => onDropPreview(layer.slot)}
              >
                <strong>{layer.slot}</strong>: {layer.itemId}
              </div>
            ))}
          </div>
        ) : (
          <div>
            <p>
              Sigkill 3D — Look Preset 동기화 미지원(베타). 수동으로 비교해 주세요.
            </p>
            <iframe
              className="depth-preview"
              src={DEPTH_URL}
              title="Depth Preview"
            />
          </div>
        )}

        {imagePreview && (
          <img
            src={imagePreview}
            alt="Reference"
            style={{ maxWidth: "100%", maxHeight: 160, objectFit: "contain" }}
          />
        )}
      </section>

      <aside className="panel">
        <h2>설정</h2>
        <label>
          Reference Image
          <input
            type="file"
            accept="image/*"
            onChange={(e) => onFile(e.target.files?.[0] ?? null)}
          />
        </label>
        <label>
          Server
          <select value={serverId} onChange={(e) => setServerId(e.target.value)}>
            <option value="mabikr1">류트 (mabikr1)</option>
          </select>
        </label>
        <label>
          Age
          <input
            type="number"
            value={base.age}
            onChange={(e) => setBase({ ...base, age: Number(e.target.value) })}
          />
        </label>
        <button type="button" disabled={!imageFile || busy} onClick={startRun}>
          Analysis Run
        </button>
        <button type="button" onClick={copyShareLink}>
          Share Link 복사
        </button>
      </aside>

      <aside className="panel" style={{ overflow: "auto", maxHeight: "90vh" }}>
        <h2>Candidate List</h2>
        {!analysis && <p>Analysis Run 후 슬롯별 후보가 표시됩니다.</p>}
        {analysis?.slots.map((slot) => (
          <div key={slot.slot_id} style={{ marginBottom: 12 }}>
            <h3>
              {slot.slot_id}{" "}
              {analysis.unrecognized_slots.includes(slot.slot_id) && (
                <span className="badge">식별 안 됨</span>
              )}
            </h3>
            {slot.candidates.length === 0 && <p>후보 없음</p>}
            {slot.candidates.map((c) => (
              <div
                key={c.id}
                className="candidate"
                draggable
                onDragStart={() => onDragStart(slot.slot_id, c)}
                onClick={() => equip(slot.slot_id, c)}
              >
                {c.display_name_ko}
                {c.dyeable ? " · 염색 가능" : ""}
              </div>
            ))}
          </div>
        ))}
      </aside>
    </main>
  );
}
