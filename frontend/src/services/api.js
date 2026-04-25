import axios from "axios";

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL ?? "http://localhost:8000",
});

export async function uploadPdf(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await apiClient.post("/upload-pdf/", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });

  return response.data;
}

export async function saveFormula(payload) {
  const response = await apiClient.post("/save-formula/", payload);
  return response.data;
}
