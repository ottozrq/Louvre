import { useRouter } from "next/router";
import React from "react";

import api from "../../../../components/api";
import ApiResourcePage from "../../../../components/api_resource_page";

export default function Introduction() {
  const router = useRouter();
  const { introduction_id } = router.query;
  return introduction_id ? (
    <ApiResourcePage
      title={`Introduction ${introduction_id}`}
      getter={() =>
        api.introductions.getIntroductionsIntroductionIdIntroductionsIntroductionIdGet(
          parseInt(introduction_id as string)
        )
      }
    ></ApiResourcePage>
  ) : (
    <div>Loading...</div>
  );
}
