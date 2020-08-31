from static_generator.static_generator import StaticGenerator
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--doc", help="Input document for processing.")
    parser.add_argument("--project-dir", help="Absolute project directory.")
    args = parser.parse_args()
    input_document_path = args.doc
    project_root = args.project_dir
    static_generator = StaticGenerator(input_document_path, project_root)
