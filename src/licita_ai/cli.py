"""Interface de linha de comando para indexar PDFs de editais."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

from pypdf import PdfReader


def extract_pdf(pdf_path: Path, input_dir: Path) -> dict[str, str | int]:
    """Extrai texto de um PDF e devolve uma linha para o CSV."""
    relative_name = str(pdf_path.relative_to(input_dir))
    try:
        reader = PdfReader(str(pdf_path))
        pages = len(reader.pages)
        text_parts = [(page.extract_text() or "").strip() for page in reader.pages]
        text = "\n\n".join(part for part in text_parts if part)
        status = "ok" if text else "sem texto extraível (PDF pode ser digitalizado)"
        return {
            "arquivo": relative_name,
            "paginas": pages,
            "caracteres_extraidos": len(text),
            "status": status,
            "texto": text,
        }
    except Exception as exc:  # Mantém o processamento dos demais PDFs.
        return {
            "arquivo": relative_name,
            "paginas": 0,
            "caracteres_extraidos": 0,
            "status": f"erro: {exc}",
            "texto": "",
        }


def index_pdfs(input_dir: Path, output_file: Path) -> int:
    """Indexa os PDFs de uma pasta e grava os textos extraídos em CSV."""
    if not input_dir.exists() or not input_dir.is_dir():
        raise NotADirectoryError(f"A pasta de entrada não existe: {input_dir}")

    pdf_files = sorted(
        (path for path in input_dir.rglob("*") if path.is_file() and path.suffix.lower() == ".pdf"),
        key=lambda path: str(path).lower(),
    )
    output_file.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "arquivo",
        "paginas",
        "caracteres_extraidos",
        "status",
        "texto",
    ]
    with output_file.open("w", encoding="utf-8-sig", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        for pdf_path in pdf_files:
            row = extract_pdf(pdf_path, input_dir)
            writer.writerow(row)
            print(f"{row['status']}: {row['arquivo']}")

    print(f"\nPDFs encontrados: {len(pdf_files)}")
    print(f"CSV criado em: {output_file}")
    return len(pdf_files)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="licita-ai",
        description="Extrai texto de PDFs de editais e cria um CSV pesquisável.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    index_parser = subparsers.add_parser("index", help="indexar PDFs de uma pasta")
    index_parser.add_argument(
        "input_dir",
        type=Path,
        help="pasta com PDFs (a busca inclui subpastas)",
    )
    index_parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/processed/editais.csv"),
        help="caminho do CSV de saída (padrão: data/processed/editais.csv)",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    try:
        index_pdfs(args.input_dir, args.output)
    except NotADirectoryError as exc:
        parser.error(str(exc))


if __name__ == "__main__":
    main()
