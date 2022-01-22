import { useRouter } from "next/router";
import React from "react";

import api from "../../../../components/api";
import ApiResourcePage from "../../../../components/api_resource_page";

export default function Artwork() {
  const router = useRouter();
  const { artwork_id } = router.query;
  return artwork_id ? (
    <ApiResourcePage
      title={`Artwork ${artwork_id}`}
      getter={() =>
        api.artworks.getArtworksArtworkIdArtworksArtworkIdGet(
          parseInt(artwork_id as string)
        )
      }
    ></ApiResourcePage>
  ) : (
    <div>Loading...</div>
  );
}
