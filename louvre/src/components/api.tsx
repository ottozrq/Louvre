import axios from "axios";

import {
  ArtworksApiFactory,
  Configuration,
  IntroductionsApiFactory,
  ImagesApiFactory,
  LandmarksApiFactory,
  RootApiFactory,
  SeriesApiFactory,
  UsersApiFactory,
} from "../api";

export const config = new Configuration({});

if (typeof window !== "undefined") {
  config.accessToken = window.localStorage.getItem("access_token") || "";
  config.basePath = "http://127.0.0.1:8000";
    // window.localStorage.getItem("base_path") || "https://vision.ottozhang.com";
}

export function setApiBasePath(s: string) {
  window.localStorage.base_path = s;
  config.basePath = s;
}

const api = {
  artworks: ArtworksApiFactory(config),
  landmarks: LandmarksApiFactory(config),
  introductions: IntroductionsApiFactory(config),
  images: ImagesApiFactory(config),
  root: RootApiFactory(config),
  series: SeriesApiFactory(config),
  users: UsersApiFactory(config),
};

axios.interceptors.response.use(
  (c) => c,
  (e) => {
    if (e?.response?.status === 401) {
      (window as unknown as any).location = "/login";
    }
  }
);

export default api;
