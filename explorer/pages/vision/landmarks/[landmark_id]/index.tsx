import { useRouter } from "next/router";
import React from "react";

import api from "../../../../components/api";
import ApiResourcePage from "../../../../components/api_resource_page";

export default function Landmark() {
  const router = useRouter();
  const { landmark_id } = router.query;
  return landmark_id ? (
    <ApiResourcePage
      title={`Landmark ${landmark_id}`}
      getter={() =>
        api.landmarks.getLandmarksLandmarkIdLandmarksLandmarkIdGet(
          parseInt(landmark_id as string)
        )
      }
    ></ApiResourcePage>
  ) : (
    <div>Loading...</div>
  );
}
