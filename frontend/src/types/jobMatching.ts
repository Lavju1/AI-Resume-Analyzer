import type { AIAnalysis } from "./resume";

export type JobMatchRequest = {
  resume_id: string;
  job_description_text: string;
};

export type JobMatchResponse = {
  overall_match: number;
  matched_skills: string[];
  missing_skills: string[];
  matched_keywords: string[];
  missing_keywords: string[];
  ai_analysis: AIAnalysis;
};
