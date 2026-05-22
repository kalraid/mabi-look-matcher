import { Suspense } from "react";
import HomeClient from "@/components/HomeClient";

export default function Page() {
  return (
    <Suspense fallback={<main style={{ padding: 12 }}>Loading...</main>}>
      <HomeClient />
    </Suspense>
  );
}
