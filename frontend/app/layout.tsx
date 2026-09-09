import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Freight Intelligence System",
  description: "AI-Powered Maritime Freight & Vessel Optimization Platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="bg-slate-900 text-slate-100 antialiased">
        <main className="min-h-screen p-6">{children}</main>
      </body>
    </html>
  );
}