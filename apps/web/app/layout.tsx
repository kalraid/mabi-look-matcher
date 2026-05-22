import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Mabi Look Matcher",
  description: "Reference image to Mabinogi outfit candidates",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  );
}
