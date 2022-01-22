import { useRouter } from "next/router";
import { useEffect } from "react";

import Layout from "../components/layout";

export function toQuerySet<T>(x: Set<T> | T[]): Set<T> {
  return [...x] as unknown as Set<T>;
}

export default function Main() {
  const router = useRouter();
  useEffect(() => void router.push("/vision"), []);
  return <Layout>Rerouting</Layout>;
}
