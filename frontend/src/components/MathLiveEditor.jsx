import { useEffect, useRef, useState } from "react";
import "mathlive";

export default function MathLiveEditor({
  latexContent,
  setLatexContent,
  selectedFormula,
  onSave,
  isSaving,
  saveMessage,
}) {
  const mathFieldRef = useRef(null);
  const [statusText, setStatusText] = useState("San sang chinh sua cong thuc.");

  useEffect(() => {
    const mathField = mathFieldRef.current;
    if (!mathField) {
      return undefined;
    }

    mathField.value = latexContent || "";

    const handleInput = () => {
      setLatexContent(mathField.value);
      setStatusText("Da dong bo du lieu tu MathLive sang LaTeX raw.");
    };

    mathField.addEventListener("input", handleInput);
    return () => mathField.removeEventListener("input", handleInput);
  }, [setLatexContent]);

  useEffect(() => {
    const mathField = mathFieldRef.current;
    if (mathField && mathField.value !== latexContent) {
      mathField.value = latexContent || "";
      setStatusText("Da dong bo du lieu tu LaTeX raw sang MathLive.");
    }
  }, [latexContent]);

  return (
    <section className="rounded-[28px] border border-slate-200 bg-white p-6 shadow-xl shadow-slate-200/60">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.25em] text-emerald-700">
            MathLive
          </p>
          <h2 className="mt-2 text-2xl font-bold text-slate-900">Trinh soan thao cong thuc</h2>
          <p className="mt-2 text-sm text-slate-600">
            Chinh sua tren MathLive hoac textarea, du lieu se dong bo hai chieu.
          </p>
        </div>
        <button
          type="button"
          onClick={onSave}
          disabled={!latexContent || isSaving}
          className="rounded-xl bg-emerald-600 px-5 py-3 text-sm font-semibold text-white transition hover:bg-emerald-700 disabled:cursor-not-allowed disabled:bg-slate-400"
        >
          {isSaving ? "Dang luu..." : "Luu"}
        </button>
      </div>

      <div className="mt-5 rounded-2xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-600">
        <p className="font-medium text-slate-700">
          {selectedFormula
            ? `Dang chinh sua cong thuc trang ${selectedFormula.page_number ?? "?"}`
            : "Chua co cong thuc nao duoc chon"}
        </p>
        {selectedFormula?.source_text ? (
          <p className="mt-2 text-xs text-slate-500">
            Text phat hien tu PDF: {selectedFormula.source_text}
          </p>
        ) : null}
        <p className="mt-2 text-xs text-slate-500">{statusText}</p>
        {saveMessage ? <p className="mt-2 text-xs text-emerald-700">{saveMessage}</p> : null}
      </div>

      <div className="mt-6 space-y-4">
        <label className="block">
          <span className="mb-2 block text-sm font-medium text-slate-700">Math Preview</span>
          <math-field
            ref={mathFieldRef}
            class="block min-h-24 w-full rounded-2xl border border-slate-300 bg-white px-4 py-4 text-lg focus:border-emerald-500 focus:outline-none"
          />
        </label>

        <label className="block">
          <span className="mb-2 block text-sm font-medium text-slate-700">LaTeX Raw</span>
          <textarea
            className="min-h-48 w-full rounded-2xl border border-slate-300 bg-slate-950 px-4 py-4 font-mono text-sm text-emerald-100 focus:border-emerald-500 focus:outline-none"
            value={latexContent}
            onChange={(event) => setLatexContent(event.target.value)}
            placeholder="Nhap hoac chinh sua chuoi LaTeX tai day..."
          />
        </label>
      </div>
    </section>
  );
}
