export interface PDFFile {
  id: string;
  name: string;
  status: "done" | "not_done";
  url: string;
  changes?: string[];
}
