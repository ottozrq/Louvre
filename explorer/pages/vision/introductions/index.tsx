import { useRouter } from "next/router";
import React from "react";

import api from "../../../components/api";
import ApiResourcePage from "../../../components/api_resource_page";
import ApiCollectionPage from "../../../components/api_collection";

export default function Landmarks() {
  const router = useRouter();
  const series_id = 1
  return (
    <ApiResourcePage
      title="Landmarks"
      getter={() => api.introductions.getSeriesSeriesIdIntroductionsSeriesSeriesIdIntroductionsGet(series_id)}
      childrenCallback={(data) => (
        <>
          <ApiCollectionPage
            collection={data}
            title={(x) => x.introduction_name}
            router={router}
          />
        </>
      )}
    ></ApiResourcePage>
  );
}
