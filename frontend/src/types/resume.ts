export type ResumeRead = {
  id: string;
  user_id: string;
  original_filename: string;
  content_type: string;
  file_size: number;
  upload_status: string;
  created_at: string;
  updated_at: string;
};

export type ResumeData = {
  name: string | null;
  email: string | null;
  phone: string | null;
  skills: string[];
  education: string[];
  experience: string[];
  projects: string[];
};

export type ATSSectionScores = {
  contact: number;
  skills: number;
  education: number;
  experience: number;
  projects: number;
};

export type ATSScore = {
  overall_score: number;
  section_scores: ATSSectionScores;
  missing_sections: string[];
  strengths: string[];
  weaknesses: string[];
};

export type FeedbackItem = {
  category: string;
  severity: "info" | "warning" | "success";
  title: string;
  message: string;
};

export type ResumeFeedback = {
  overall_summary: string;
  feedback: FeedbackItem[];
};

export type AIAnalysis = {
  summary: string;
  strengths: string[];
  weaknesses: string[];
  recommendations: string[];
};

export type ResumeUploadResponse = {
  resume: ResumeRead;
  parsed_text: string;
  extracted_data: ResumeData;
  ats_score: ATSScore;
  feedback: ResumeFeedback;
  ai_analysis: AIAnalysis;
};
