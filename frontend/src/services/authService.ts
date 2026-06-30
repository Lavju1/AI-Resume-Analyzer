import { apiClient } from "../api/client";
import type { LoginPayload, RegisterPayload, Token, User } from "../types/auth";

export const authService = {
  async login(payload: LoginPayload): Promise<Token> {
    const response = await apiClient.post<Token>("/auth/login", payload);
    return response.data;
  },

  async register(payload: RegisterPayload): Promise<User> {
    const response = await apiClient.post<User>("/auth/register", payload);
    return response.data;
  },

  async getCurrentUser(): Promise<User> {
    const response = await apiClient.get<User>("/auth/me");
    return response.data;
  },
};
