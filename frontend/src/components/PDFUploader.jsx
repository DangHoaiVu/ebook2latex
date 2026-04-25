import { useState } from "react";

import { uploadPdf } from "../services/api";

export default function PDFUploader({ onUploadSuccess, selectedFormulaId, onSelectFormula }) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState(null);
  const [error, setError] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!selectedFile) {
      return;
    }

    setIsUploading(true);
    setError("");

    try {
      const result = await uploadPdf(selectedFile);
      setUploadResult(result);
      onUploadSuccess(result);
    } catch (err) {
      setError(err.response?.data?.detail ?? err.message ?? "Khong the tai file PDF");
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <section className="rounded-[28px] border border-slate-200 bg-white p-6 shadow-xl shadow-slate-200/60">
      <p className="text-xs font-semibold uppercase tracking-[0.25em] text-sky-700">Parse Tool</p>
      <h2 className="mt-2 text-2xl font-bold text-slate-900">Tai PDF va OCR cong thuc</h2>
      <p className="mt-2 text-sm text-slate-600">
        Luong xu ly: upload PDF, cat anh cong thuc bang PyMuPDF, OCR sang LaTeX bang
        pix2tex.
      </p>

      <form className="mt-6 space-y-4" onSubmit={handleSubmit}>
        <input
          type="file"
          accept=".pdf"
          className="block w-full rounded-2xl border border-dashed border-slate-300 bg-slate-50 px-4 py-6 text-sm text-slate-700 file:mr-4 file:rounded-xl file:border-0 file:bg-sky-600 file:px-4 file:py-2 file:text-sm file:font-medium file:text-white hover:file:bg-sky-700"
          onChange={(event) => setSelectedFile(event.target.files?.[0] ?? null)}
        />
        <button
          type="submit"
          disabled={!selectedFile || isUploading}
          className="rounded-xl bg-slate-900 px-5 py-3 text-sm font-semibold text-white transition hover:bg-slate-700 disabled:cursor-not-allowed disabled:bg-slate-400"
        >
          {isUploading ? "Dang phan tich..." : "Upload PDF"}
        </button>
      </form>

      {error ? (
        <div className="mt-4 rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
          {error}
        </div>
      ) : null}

      {uploadResult ? (
        <div className="mt-6">
          <div className="rounded-2xl border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-800">
            <p className="font-semibold">{uploadResult.message}</p>
            <p className="mt-2">Document ID: {uploadResult.document_id}</p>
            <p>Ten file: {uploadResult.file_name}</p>
            <p>So trang: {uploadResult.total_pages}</p>
          </div>

          <div className="mt-5">
            <h3 className="text-sm font-semibold uppercase tracking-[0.2em] text-slate-500">
              Danh sach cong thuc
            </h3>
            <div className="mt-3 space-y-3">
              {uploadResult.formulas?.map((formula) => (
                <button
                  key={formula.id}
                  type="button"
                  onClick={() => onSelectFormula(formula)}
                  className={`w-full rounded-2xl border p-4 text-left transition ${
                    selectedFormulaId === formula.id
                      ? "border-sky-500 bg-sky-50"
                      : "border-slate-200 bg-slate-50 hover:border-slate-300"
                  }`}
                >
                  <p className="text-sm font-semibold text-slate-800">
                    Formula #{formula.id.slice(0, 8)}
                  </p>
                  <p className="mt-1 text-xs text-slate-500">Trang: {formula.page_number ?? "?"}</p>
                  <p className="mt-3 rounded-xl bg-slate-900 px-3 py-2 font-mono text-xs text-emerald-100">
                    {formula.latex || "Chua co ket qua OCR"}
                  </p>
                </button>
              ))}
            </div>
          </div>
        </div>
      ) : null}
    </section>
  );
}
