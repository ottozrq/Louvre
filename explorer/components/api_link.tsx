import Link from "next/link";
import React from "react";

interface ApiLinkInput {
  value: string;
  text?: string;
  children?: unknown;
}
export default function ApiLink({ text, value, children }: ApiLinkInput) {
  return (
    <Link href={`/vision${value.replace(".", "_")}`}>
      <a>
        {text || value}
        {children}
      </a>
    </Link>
  );
}
