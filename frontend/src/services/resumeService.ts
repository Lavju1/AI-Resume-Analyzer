import type { AxiosProgressEvent } from "axios";

import { apiClient } from "../api/client";
import type { ResumeRead, ResumeUploadResponse } from "../types/resume";

type UploadResumeOptions = {
  onUploadProgress?: (event: AxiosProgressEvent) => void;
};

export const resumeService = {
  async listResumes(): Promise<ResumeRead[]> {
    const response = await apiClient.get<ResumeRead[]>("/resumes");
    return response.data;
  },

  async uploadResume(
    file: File,
    options: UploadResumeOptions = {},
  ): Promise<ResumeUploadResponse> {
    const formData = new FormData();
    formData.append("file", file);

    const response = await apiClient.post<ResumeUploadResponse>(
      "/resumes/upload",
      formData,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
        onUploadProgress: options.onUploadProgress,
      },
    );

    return response.data;
  },
};
