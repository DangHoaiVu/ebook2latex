import { useState } from "react";

import MathLiveEditor from "./components/MathLiveEditor";
import PDFUploader from "./components/PDFUploader";
import { saveFormula } from "./services/api";

export default function App() {
  const [uploadResult, setUploadResult] = useState(null);
  const [selectedFormula, setSelectedFormula] = useState(null);
  const [latexContent, setLatexContent] = useState("");
  const [isSaving, setIsSaving] = useState(false);
  const [saveMessage, setSaveMessage] = useState("");

  const handleUploadSuccess = (result) => {
    setUploadResult(result);
    const firstFormula = result.formulas?.[0] ?? null;
    setSelectedFormula(firstFormula);
    setLatexContent(firstFormula?.latex ?? "");
    setSaveMessage("");
  };

  const handleSelectFormula = (formula) => {
    setSelectedFormula(formula);
    setLatexContent(formula?.latex ?? "");
    setSaveMessage("");
  };

  const handleSave = async () => {
    if (!uploadResult?.document_id || !latexContent) {
      return;
    }

    setIsSaving(true);
    setSaveMessage("");

    try {
      const result = await saveFormula({
        document_id: uploadResult.document_id,
        formula_entry_id: selectedFormula?.id ?? null,
        latex_result: latexContent,
      });

      setSaveMessage(result.message);

      if (selectedFormula) {
        setSelectedFormula({
          ...selectedFormula,
          id: result.formula_entry_id,
          latex: result.latex_result,
        });
      }

      setUploadResult((previous) => {
        if (!previous) {
          return previous;
        }

        const alreadyExists = previous.formulas.some(
          (formula) => formula.id === result.formula_entry_id
        );

        if (!alreadyExists) {
          return {
            ...previous,
            formulas: [
              ...previous.formulas,
              {
                id: result.formula_entry_id,
                page_number: selectedFormula?.page_number ?? null,
                image_path: selectedFormula?.image_path ?? null,
                latex: result.latex_result,
                source_text: selectedFormula?.source_text ?? null,
              },
            ],
          };
        }

        return {
          ...previous,
          formulas: previous.formulas.map((formula) =>
            formula.id === result.formula_entry_id
              ? { ...formula, latex: result.latex_result }
              : formula
          ),
        };
      });
    } catch (err) {
      setSaveMessage(err.response?.data?.detail ?? "Khong the luu cong thuc");
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_top,_#e0f2fe,_#f8fafc_45%,_#e2e8f0_100%)] px-6 py-10">
      <div className="mx-auto max-w-7xl">
        <header className="mb-8 rounded-[32px] border border-white/70 bg-white/80 p-8 shadow-2xl shadow-slate-200/60 backdrop-blur">
          <p className="text-xs font-semibold uppercase tracking-[0.35em] text-sky-700">Lab 3</p>
          <div className="mt-4 flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between">
            <div>
              <h1 className="text-4xl font-bold text-slate-900">Ebook2LateX - Local Workflow</h1>
              <p className="mt-3 max-w-3xl text-lg text-slate-600">
                Chay tren Windows local voi FastAPI, PostgreSQL va React/Vite. Nguoi dung
                upload PDF, trich xuat cong thuc, OCR sang LaTeX, chinh sua va luu lai.
              </p>
            </div>
            <div className="grid grid-cols-2 gap-4 rounded-2xl bg-slate-950 p-4 text-slate-100">
              <div>
                <p className="text-xs uppercase tracking-[0.2em] text-slate-400">Document</p>
                <p className="mt-2 text-2xl font-bold">{uploadResult ? 1 : 0}</p>
              </div>
              <div>
                <p className="text-xs uppercase tracking-[0.2em] text-slate-400">Formula</p>
                <p className="mt-2 text-2xl font-bold">{uploadResult?.formulas?.length ?? 0}</p>
              </div>
            </div>
          </div>
        </header>

        <div className="grid gap-6 lg:grid-cols-[0.95fr,1.25fr]">
          <PDFUploader
            onUploadSuccess={handleUploadSuccess}
            selectedFormulaId={selectedFormula?.id}
            onSelectFormula={handleSelectFormula}
          />

          <MathLiveEditor
            latexContent={latexContent}
            setLatexContent={setLatexContent}
            selectedFormula={selectedFormula}
            onSave={handleSave}
            isSaving={isSaving}
            saveMessage={saveMessage}
          />
        </div>
      </div>
    </main>
  );
}
