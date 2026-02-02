from __future__ import annotations
from pathlib import Path
from typing import List, Tuple, Optional
import json

import pandas as pd
from pypdf import PdfReader


def load_pdf(path: Path) -> str:
    reader = PdfReader(str(path))
    parts = []
    for page in reader.pages:
        txt = page.extract_text() or ""
        if txt.strip():
            parts.append(txt)
    return "\n".join(parts)


def load_xlsx(path: Path) -> str:
    xls = pd.ExcelFile(path)
    blocks = []
    for sheet in xls.sheet_names:
        df = xls.parse(sheet)
        blocks.append(f"--- SHEET: {sheet} ---\n{df.to_csv(index=False)}")
    return "\n\n".join(blocks)


def load_json(path: Path) -> str:
    obj = json.loads(path.read_text(encoding="utf-8"))
    return json.dumps(obj, ensure_ascii=False, indent=2)


def load_txt(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def load_any(path: Path) -> Optional[str]:
    suffix = path.suffix.lower()
    try:
        if suffix == ".pdf":
            return load_pdf(path)
        if suffix in (".xlsx", ".xls"):
            return load_xlsx(path)
        if suffix == ".json":
            return load_json(path)
        if suffix in (".txt", ".md"):
            return load_txt(path)
    except Exception:
        # Fail-safe: if a file is corrupted, ignore it rather than crashing ingestion
        return None
    return None


def list_documents(docs_dir: Path) -> List[Tuple[Path, str]]:
    if not docs_dir.exists():
        return []
    out: List[Tuple[Path, str]] = []
    for p in docs_dir.rglob("*"):
        if p.is_file():
            text = load_any(p)
            if text and text.strip():
                out.append((p, text))
    return out
