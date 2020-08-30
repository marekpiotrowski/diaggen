from static_generator.static_generator import StaticGenerator
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--doc", help="Input document for processing.")
    args = parser.parse_args()
    input_document_path = args.doc
    static_generator = StaticGenerator(input_document_path)
