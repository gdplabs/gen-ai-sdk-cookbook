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
      <head>
        {/* eslint-disable-next-line @next/next/no-page-custom-font */}
        <link
          href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="bg-white antialiased">{children}ii</body>
    </html>
  );
}
