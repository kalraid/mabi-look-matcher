import type { BaseCharacter, EquippedState, LookPresetPayload } from "./types";

function toBase64Url(bytes: Uint8Array): string {
  let binary = "";
  bytes.forEach((b) => {
    binary += String.fromCharCode(b);
  });
  return btoa(binary).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

function fromBase64Url(token: string): Uint8Array {
  const padded = token.replace(/-/g, "+").replace(/_/g, "/");
  const pad = padded.length % 4 === 0 ? padded : padded + "=".repeat(4 - (padded.length % 4));
  const binary = atob(pad);
  const out = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) out[i] = binary.charCodeAt(i);
  return out;
}

export function encodePreset(
  serverId: string,
  region: string,
  base: BaseCharacter,
  equipped: EquippedState
): string {
  const equippedPayload: LookPresetPayload["equipped"] = {};
  for (const [slot, item] of Object.entries(equipped)) {
    const row: { id: string; hint?: number[]; over?: number[] } = { id: item.itemId };
    if (item.dyeHint) row.hint = item.dyeHint;
    if (item.dyeOverride) row.over = item.dyeOverride;
    equippedPayload[slot] = row;
  }

  const payload: LookPresetPayload = {
    v: 1,
    server: { server_id: serverId, region },
    base,
    equipped: equippedPayload,
  };

  const json = JSON.stringify(payload);
  const compressed = json; // browser zlib optional later; API codec uses zlib
  return toBase64Url(new TextEncoder().encode(compressed));
}

export function decodePresetFromUrl(param: string | null): LookPresetPayload | null {
  if (!param) return null;
  try {
    const bytes = fromBase64Url(param);
    const json = new TextDecoder().decode(bytes);
    const data = JSON.parse(json) as LookPresetPayload;
    if (data.v !== 1) return null;
    return data;
  } catch {
    return null;
  }
}

export function presetToEquipped(data: LookPresetPayload): EquippedState {
  const out: EquippedState = {};
  for (const [slot, row] of Object.entries(data.equipped)) {
    out[slot] = {
      itemId: row.id,
      dyeable: Boolean(row.hint || row.over),
      dyeHint: row.hint as [number, number, number] | undefined,
      dyeOverride: row.over as [number, number, number] | undefined,
    };
  }
  return out;
}
