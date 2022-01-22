import { AxiosPromise } from "axios";
import React, { useEffect, useState } from "react";

import ApiLinks from "./api_links";
import Layout from "./layout";

interface ApiResourcePageProps<T> {
  title: string;
  getter(): AxiosPromise<T>;
  childrenCallback?(data: T);
  children?;
  updateString?: string;
}

export default function ApiResourcePage<T>({
  childrenCallback,
  children,
  getter,
  title,
  updateString,
}: ApiResourcePageProps<T>) {
  const [data, setData] = useState(null as T);
  useEffect(() => {
    async function f() {
      setData((await getter()).data);
    }
    f();
  }, [updateString]);
  return (
    <Layout title={title}>
      {!data ? (
        <div>Loading...</div>
      ) : (
        <div>
          <h1>{title}</h1>
          {children}
          {childrenCallback ? childrenCallback(data) : []}
          <ApiLinks resource={data} />
        </div>
      )}
    </Layout>
  );
}
