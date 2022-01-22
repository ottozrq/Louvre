import { useRouter } from "next/router";
import React from "react";

import api from "../../../components/api";
import ApiResourcePage from "../../../components/api_resource_page";
import ApiCollectionPage from "../../../components/api_collection";

export default function Landmarks() {
  const router = useRouter();
  return (
    <ApiResourcePage
      title="Landmarks"
      getter={() => api.landmarks.getLandmarksLandmarksGet()}
      childrenCallback={(data) => (
        <>
          <ApiCollectionPage
            collection={data}
            title={(x) => x.landmark_name["en"]}
            router={router}
          />
        </>
      )}
    ></ApiResourcePage>
  );
}
