---
name: testing-verification
description: Assists in generating test boilerplate (unit, integration, smoke) and guides on testing strategies (pyramid, types, mocking, patterns). Use when creating new tests, analyzing existing test suites, or defining testing approaches.
---

# Testing Verification

## Overview

This skill provides guidance and tools to assist in creating, executing, and analyzing a robust testing strategy for your projects. It covers generating test boilerplate and offering insights into various testing methodologies.

## Test Generation Assistance

This section provides tools to help you quickly set up different types of tests.

### Generate Unit Tests

Use this to create boilerplate for unit tests.
*   **Python (`unittest` or `pytest` style):**
    ```bash
    node .gemini/skills/testing-verification/scripts/generate_unit_test_py.py --class_name <ClassName> --function_name <function_name> --output_file <path/to/test_file.py>
    ```
    Reference template: [unit_test_template_py.txt](assets/unit_test_template_py.txt)

### Generate Integration Tests

Use this to create boilerplate for integration tests.
*   **Python (`unittest` style):**
    ```bash
    node .gemini/skills/testing-verification/scripts/generate_integration_test_py.py --component_name <ComponentName> --interaction_description <brief_description_of_interaction> --output_file <path/to/test_integration_file.py>
    ```
    Reference template: [integration_test_template_py.txt](assets/integration_test_template_py.txt)

### Generate Smoke Tests

Use this to create a simple shell script for smoke tests.
*   **Bash Script:**
    ```bash
    node .gemini/skills/testing-verification/scripts/generate_smoke_test_sh.sh --url <application_url> --output <path/to/smoke_test.sh> [--status <expected_status>] [--content <expected_content_snippet>]
    ```
    Reference template: [smoke_test_template_sh.txt](assets/smoke_test_template_sh.txt)

## Test Analysis & Strategy Guidance

These references provide best practices and conceptual frameworks for designing effective testing strategies.

*   **The Testing Pyramid:** Understand how to balance different test types for optimal feedback and cost.
    *   See: [testing_pyramid_guide.md](references/testing_pyramid_guide.md)
*   **Test Types and Strategies:** Detailed descriptions of various test types (unit, integration, E2E, smoke, performance, security) and strategic approaches.
    *   See: [test_types_strategies.md](references/test_types_strategies.md)
*   **Mocking and Stubbing:** Best practices for isolating components and controlling dependencies in tests.
    *   See: [mocking_stubbing_guide.md](references/mocking_stubbing_guide.md)
*   **Common Test Patterns:** Learn about patterns like Arrange-Act-Assert (AAA) and Given-When-Then (GWT).
    *   See: [common_test_patterns.md](references/common_test_patterns.md)

## Resources

This skill bundles the following resources:

### scripts/
- `generate_unit_test_py.py`: Python script for generating unit test boilerplate.
- `generate_integration_test_py.py`: Python script for generating integration test boilerplate.
- `generate_smoke_test_sh.sh`: Bash script for generating smoke test scripts.

### references/
- `testing_pyramid_guide.md`: Guidance on the testing pyramid.
- `test_types_strategies.md`: Documentation on various test types and strategies.
- `mocking_stubbing_guide.md`: Best practices for mocking and stubbing.
- `common_test_patterns.md`: Overview of common test patterns.

### assets/
- `unit_test_template_py.txt`: Template for Python unit tests.
- `integration_test_template_py.txt`: Template for Python integration tests.
- `smoke_test_template_sh.txt`: Template for Bash smoke tests.