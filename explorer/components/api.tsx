import axios from "axios";

import {
  ArtworksApiFactory,
  Configuration,
  IntroductionApiFactory,
  ImagesApiFactory,
  LandmarksApiFactory,
  RootApiFactory,
  SeriesApiFactory,
} from "../api";

export const config = new Configuration({});

if (typeof window !== "undefined") {
  config.accessToken = window.localStorage.getItem("access_token");
  config.basePath =
    window.localStorage.getItem("base_path") || "https://vision.ottozhang.com";
}

export function setApiBasePath(s: string) {
  window.localStorage.base_path = s;
  config.basePath = s;
}

const api = {
  artworks: ArtworksApiFactory(config),
  landmarks: LandmarksApiFactory(config),
  introductions: IntroductionApiFactory(config),
  images: ImagesApiFactory(config),
  root: RootApiFactory(config),
  series: SeriesApiFactory(config),
};

axios.interceptors.response.use(
  (c) => c,
  (e) => {
    if (e?.response?.status === 401) {
      (window as unknown as any).location = "/vision/token";
    }
  }
);

export default api;
