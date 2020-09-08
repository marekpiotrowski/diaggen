import argparse
import os

from static_generator.static_generator import StaticGenerator
from common.md_with_puml_to_pdf_generator import MdWithPumlToPdfGenerator


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-dir", help="Absolute project directory.", required=True)
    parser.add_argument("--doc", help="Input document for processing (relative to project dir).", required=True)
    args = parser.parse_args()
    relative_input_document_path = args.doc
    project_root = args.project_dir
    # todo it's assumed that input md document will end with .in!
    static_generator = StaticGenerator(project_root, relative_input_document_path)
    pdf_generator = MdWithPumlToPdfGenerator()
    pdf_generator.generate(os.path.join(project_root, relative_input_document_path.replace('.in', '')))
