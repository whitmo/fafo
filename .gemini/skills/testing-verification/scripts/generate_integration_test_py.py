#!/usr/bin/env python3

import argparse
import os

def generate_integration_test_py(component_name: str, interaction_description: str, output_file: str):
    """
    Generates a Python integration test file based on a template.
    """
    script_dir = os.path.dirname(__file__)
    template_path = os.path.join(script_dir, "../assets/integration_test_template_py.txt")

    try:
        with open(template_path, 'r') as f:
            template_content = f.read()

        generated_content = template_content.replace("{{COMPONENT_NAME}}", component_name)
        generated_content = generated_content.replace("{{INTERACTION_DESCRIPTION}}", interaction_description)

        with open(output_file, 'w') as f:
            f.write(generated_content)
        print(f"Success: Python integration test generated at '{output_file}' for component '{component_name}' and interaction '{interaction_description}'.")
    except FileNotFoundError:
        print(f"Error: Template file not found at '{template_path}'.")
    except Exception as e:
        print(f"Error generating integration test: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a Python integration test file.")
    parser.add_argument("--component_name", required=True, help="Name of the main component under test.")
    parser.add_argument("--interaction_description", required=True, help="Brief description of the interaction being tested.")
    parser.add_argument("--output_file", required=True, help="Path to the output test file (e.g., tests/test_integration.py).")
    args = parser.parse_args()

    generate_integration_test_py(args.component_name, args.interaction_description, args.output_file)
