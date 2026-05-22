export type BaseCharacter = {
  race: string;
  gender: string;
  age: number;
};

export type Candidate = {
  id: string;
  display_name_ko: string;
  dyeable: boolean;
  thumbnail_url: string | null;
  slot_ids: string[];
};

export type SlotResult = {
  slot_id: string;
  status: string;
  candidates: Candidate[];
  message?: string;
};

export type AnalysisRunResponse = {
  run_id: string;
  status: string;
  server_id: string;
  unrecognized_slots: string[];
  slots: SlotResult[];
};

export type EquippedState = Record<
  string,
  {
    itemId: string;
    dyeable: boolean;
    dyeHint?: [number, number, number];
    dyeOverride?: [number, number, number];
  }
>;

export type LookPresetPayload = {
  v: number;
  server: { server_id: string; region: string };
  base: BaseCharacter;
  equipped: Record<
    string,
    { id: string; hint?: number[]; over?: number[] }
  >;
};
