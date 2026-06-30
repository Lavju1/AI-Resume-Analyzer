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

export type ResumeUploadResponse = {
  resume: ResumeRead;
  parsed_text: string;
  extracted_data: unknown;
  ats_score: unknown;
  feedback: unknown;
  ai_analysis: unknown;
};
