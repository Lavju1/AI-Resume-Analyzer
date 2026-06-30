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

export type ATSCategoryScore = {
  score: number;
  max_score: number;
  feedback: string;
};

export type ATSSectionScores = {
  contact_information: ATSCategoryScore;
  professional_summary: ATSCategoryScore;
  skills: ATSCategoryScore;
  education: ATSCategoryScore;
  experience: ATSCategoryScore;
  projects: ATSCategoryScore;
  keywords: ATSCategoryScore;
  action_verbs: ATSCategoryScore;
  quantified_achievements: ATSCategoryScore;
  formatting: ATSCategoryScore;
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
