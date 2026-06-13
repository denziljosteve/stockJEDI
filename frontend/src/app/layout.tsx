import type { Metadata } from "next";
import "./globals.css";
import Providers from "./Providers";
import Navbar from "@/components/layout/Navbar";
import Footer from "@/components/layout/Footer";

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
      <body className="antialiased bg-gray-50 text-gray-900 flex flex-col min-h-screen">
        <Providers>
          <Navbar />
          <main className="flex-grow container mx-auto px-4 py-8">
            {children}
          </main>
          <Footer />
        </Providers>
      </body>
    </html>
  );
}
