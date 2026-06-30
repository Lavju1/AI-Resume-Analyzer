import { apiClient } from "../api/client";
import type { JobMatchRequest, JobMatchResponse } from "../types/jobMatching";

export const jobMatchingService = {
  async matchResumeToJob(payload: JobMatchRequest): Promise<JobMatchResponse> {
    const response = await apiClient.post<JobMatchResponse>(
      "/resumes/job-match",
      payload,
    );
    return response.data;
  },
};
