import argparse
import logging
from pathlib import Path
from docling.document_converter import DocumentConverter

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

def convert(docx, outdir):
    logger.info('Converting %s to markdown in %s directory...', docx, outdir)
    converter = DocumentConverter()
    result = converter.convert(docx)
    with (outdir / f"{result.input.file.stem}.md").open("w") as fp:
            fp.write(result.document.export_to_markdown())

def main():
    parser = argparse.ArgumentParser(description="Convert MS Word document to Markdown.")
    parser.add_argument("docx", type=str, help="Path to the Word document")
    parser.add_argument("-o", "--out", type=str, help="Output directory")
    args = parser.parse_args()

    src_file = Path(args.docx)
    out_path = None
    if args.out:
        out_path = Path(args.out)
    else:
        out_path = Path("build")
    out_path.mkdir(exist_ok=True)

    convert(src_file, out_path)


if __name__ == "__main__":
    main()
