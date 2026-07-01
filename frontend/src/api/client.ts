import axios, { AxiosHeaders } from "axios";

import { getAccessToken } from "../utils/tokenStorage";

const configuredApiBaseUrl = import.meta.env.VITE_API_BASE_URL;

if (import.meta.env.PROD && !configuredApiBaseUrl) {
  throw new Error("VITE_API_BASE_URL must be configured for production builds.");
}

const API_BASE_URL = (configuredApiBaseUrl ?? "http://localhost:8000").replace(
  /\/+$/,
  "",
);

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

apiClient.interceptors.request.use((config) => {
  const token = getAccessToken();

  if (token) {
    config.headers = AxiosHeaders.from(config.headers);
    config.headers.set("Authorization", `Bearer ${token}`);
  }

  return config;
});
