import type { Metadata } from "next";
import "./globals.css";
import Providers from "./Providers";
import Navbar from "@/components/layout/Navbar";

export const metadata: Metadata = {
  title: "stockJEDI",
  description: "AI-Powered Stock Intelligence and Investment Analysis Platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased bg-gray-50 text-gray-900">
        <Providers>
          <Navbar />
          <main className="min-h-screen container mx-auto px-4 py-8">
            {children}
          </main>
        </Providers>
      </body>
    </html>
  );
}
