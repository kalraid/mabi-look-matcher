import type { AnalysisRunResponse, BaseCharacter } from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export async function startAnalysisRun(
  image: File,
  serverId: string,
  base: BaseCharacter
): Promise<string> {
  const form = new FormData();
  form.append("image", image);
  form.append("server_id", serverId);
  form.append("base_meta", JSON.stringify(base));

  const res = await fetch(`${API_BASE}/api/analysis/run`, {
    method: "POST",
    body: form,
  });
  if (!res.ok) throw new Error(`analysis start failed: ${res.status}`);
  const data = await res.json();
  return data.run_id as string;
}

export async function getAnalysisRun(runId: string): Promise<AnalysisRunResponse> {
  const res = await fetch(`${API_BASE}/api/analysis/run/${runId}`);
  if (!res.ok) throw new Error(`analysis poll failed: ${res.status}`);
  return res.json();
}
