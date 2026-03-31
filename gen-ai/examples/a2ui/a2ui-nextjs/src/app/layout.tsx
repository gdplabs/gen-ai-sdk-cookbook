import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "A2UI Chat Assistant",
  description: "A2UI demo chat application",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="bg-white antialiased">{children}</body>
    </html>
  );
}
