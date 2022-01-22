import { useRouter } from "next/router";
import React from "react";

import api from "../../../../components/api";
import ApiResourcePage from "../../../../components/api_resource_page";

export default function Series() {
  const router = useRouter();
  const { series_id } = router.query;
  return series_id ? (
    <ApiResourcePage
      title={`Series ${series_id}`}
      getter={() =>
        api.series.getSeriesSeriesIdSeriesSeriesIdGet(
          parseInt(series_id as string)
        )
      }
    ></ApiResourcePage>
  ) : (
    <div>Loading...</div>
  );
}
