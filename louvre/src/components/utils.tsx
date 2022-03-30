import { UserRole } from '../api';

import { config } from './api';

export const lang: string = "cn";

export const getTranslate = (obj?: object) => {
  if (obj) {
    const parsed = JSON.parse(JSON.stringify(obj))
    return parsed ? parsed[lang] ? parsed[lang] : parsed["en"] : "";
  }
  return ""
}

export const toJson = (obj?: object) => {
  if (obj)
    return JSON.parse(JSON.stringify(obj))
  return {}
}

export const getImageUrl = (uri?: string) => {
  if (uri)
    return (config.basePath ? config.basePath : "") + "/images/" + uri;
  return ""
}

export const logout = () => {
  window.localStorage.removeItem("access_token");
  config.accessToken = undefined;
}

export const login = (accessToken: string) => {
  window.localStorage.setItem("access_token", accessToken);
  config.accessToken = accessToken;
}

const decodedToken = () => {
  if (!config.accessToken)
    return false;
  const base64Url = config.accessToken.toString().split(".")[1];
  const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
  const jsonPayload = decodeURIComponent(atob(base64).split('').map(function (c) {
    return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
  }).join(""));
  return JSON.parse(jsonPayload);
}

export const validateUserToken = () => {
  if (decodedToken()["exp"] >= Date.now()) {
    logout();
    return false;
  }
  return true;
}

export const isAdmin = () => {
  if (decodedToken()["role"] === UserRole.Admin)
    return true
  return false
}

export const isEditor = () => {
  if (decodedToken()["role"] === UserRole.Admin || decodedToken()["exp"] === UserRole.Editor)
    return true
  return false
}