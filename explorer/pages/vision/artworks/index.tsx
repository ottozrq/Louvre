import { useRouter } from "next/router";
import React from "react";

import api from "../../../components/api";
import ApiResourcePage from "../../../components/api_resource_page";
import ApiCollectionPage from "../../../components/api_collection";

export default function Artworks() {
  const router = useRouter();
  const landmark_id = 1;
  return (
    <ApiResourcePage
      title="Artworks"
      getter={() => api.artworks.getArtworksLandmarksLandmarkIdArtworksGet(landmark_id)}
      childrenCallback={(data) => (
        <>
          <ApiCollectionPage
            collection={data}
            title={(x) => x.artwork_name["en"]}
            router={router}
          />
        </>
      )}
    ></ApiResourcePage>
  );
}
