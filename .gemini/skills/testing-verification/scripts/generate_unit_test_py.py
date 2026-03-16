#!/usr/bin/env python3

import argparse
import os

def generate_unit_test_py(class_name: str, function_name: str, output_file: str):
    """
    Generates a Python unit test file based on a template.
    """
    script_dir = os.path.dirname(__file__)
    template_path = os.path.join(script_dir, "../assets/unit_test_template_py.txt")

    try:
        with open(template_path, 'r') as f:
            template_content = f.read()

        generated_content = template_content.replace("{{CLASS_NAME}}", class_name)
        generated_content = generated_content.replace("{{FUNCTION_NAME}}", function_name)

        with open(output_file, 'w') as f:
            f.write(generated_content)
        print(f"Success: Python unit test generated at '{output_file}' for class '{class_name}' and function '{function_name}'.")
    except FileNotFoundError:
        print(f"Error: Template file not found at '{template_path}'.")
    except Exception as e:
        print(f"Error generating unit test: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a Python unit test file.")
    parser.add_argument("--class_name", required=True, help="Name of the class to test.")
    parser.add_argument("--function_name", required=True, help="Name of the function within the class to test.")
    parser.add_argument("--output_file", required=True, help="Path to the output test file (e.g., tests/test_my_module.py).")
    args = parser.parse_args()

    generate_unit_test_py(args.class_name, args.function_name, args.output_file)
