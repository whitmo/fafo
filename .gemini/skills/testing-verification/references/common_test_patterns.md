# Common Test Patterns

Effective testing often follows established patterns that improve the readability, maintainability, and reliability of your test suite. Understanding and applying these patterns can significantly enhance your testing efforts.

## 1. Arrange-Act-Assert (AAA)

This is a fundamental pattern for structuring individual test cases, especially unit tests.

*   **Arrange:** Set up the test state, create objects, initialize variables, and mock dependencies. This is where you prepare everything needed for the test.
*   **Act:** Perform the action or call the method/function that you are testing.
*   **Assert:** Verify that the outcome of the action is as expected. This involves checking return values, object states, or interactions with mocks.

**Benefits:**
*   **Clarity:** Makes the purpose of each part of the test explicit.
*   **Readability:** Tests are easier to understand at a glance.
*   **Maintainability:** Easier to modify or debug tests when their structure is consistent.

**Example (Python Pytest):**
```python
def test_add_two_numbers():
    # Arrange
    a = 2
    b = 3
    expected_sum = 5

    # Act
    actual_sum = a + b

    # Assert
    assert actual_sum == expected_sum
```

## 2. Given-When-Then (GWT) / Behavior-Driven Development (BDD)

Similar to AAA, but often used for higher-level tests (integration, acceptance, E2E) and is part of Behavior-Driven Development (BDD). It emphasizes clarity and collaboration by describing features in a human-readable format.

*   **Given:** The initial context or state of the system before the action.
*   **When:** The event or action that triggers the behavior under test.
*   **Then:** The expected outcome or resulting state of the system.

**Benefits:**
*   **Business Readable:** Tests can be understood by non-technical stakeholders.
*   **Collaboration:** Facilitates discussion between developers, QA, and business analysts.
*   **Focus on Behavior:** Encourages testing observable behaviors rather than internal implementation.

**Example (using a hypothetical Gherkin-like syntax in Python):**
```python
# Feature: User Authentication
#   As a user
#   I want to log in
#   So that I can access my account

def test_successful_login():
    # Given: a registered user "john.doe" with password "password123"
    user = create_registered_user("john.doe", "password123")
    login_page = LoginPage()

    # When: John enters correct credentials and clicks login
    login_page.enter_credentials(user.username, "password123")
    login_page.click_login_button()

    # Then: John should be redirected to the dashboard
    assert dashboard_page.is_displayed()
    assert dashboard_page.get_welcome_message() == f"Welcome, {user.username}!"
```

## 3. Test Doubles (Mocks, Stubs, Fakes, Spies)

As covered in the Mocking and Stubbing Guide, test doubles are crucial for isolating components and controlling test environments.

**Benefits:**
*   **Isolation:** Reduces dependencies on external systems or complex objects.
*   **Speed:** Avoids slow I/O operations (network, disk, database).
*   **Determinism:** Ensures tests are repeatable and not affected by external state changes.

## 4. Test Data Builders / Object Mother

This pattern helps in creating complex test data objects, especially when the object has many fields or dependencies.

*   **Test Data Builder:** A class or function that allows you to construct valid instances of an object step-by-step, often providing default values for most fields and allowing specific overrides for relevant fields.
*   **Object Mother:** A class that provides a set of factory methods for creating different variants of an object, pre-configured for common test scenarios.

**Benefits:**
*   **Reduced Duplication:** Avoids repeating complex object creation logic in every test.
*   **Readability:** Test data setup becomes clearer.
*   **Maintainability:** Easier to update test data when object schemas change.

**Example (Python):**
```python
class UserBuilder:
    def __init__(self):
        self.user = {"id": "1", "name": "Default User", "email": "default@example.com", "active": True}

    def with_id(self, user_id):
        self.user["id"] = user_id
        return self

    def with_name(self, name):
        self.user["name"] = name
        return self
    
    def inactive(self):
        self.user["active"] = False
        return self

    def build(self):
        return self.user

def test_inactive_user_cannot_login():
    # Arrange
    inactive_user = UserBuilder().inactive().with_name("Inactive John").build()
    # ... create a mock auth service with this user ...

    # Act
    # ... attempt login ...

    # Assert
    # ... assert login fails ...
```

## 5. Golden Master / Snapshot Testing

This pattern is useful for testing code that generates complex output (e.g., UI components, generated reports, complex data structures) where manually asserting every detail is cumbersome.

*   **Process:**
    1.  Run the code under test for a specific input.
    2.  Capture its output as a "golden master" or "snapshot."
    3.  On subsequent test runs, generate the output again and compare it byte-for-byte or line-by-line with the stored golden master.
*   **Benefits:**
    *   **Easy to Create:** Quickly captures expected output.
    *   **Detects Unexpected Changes:** Catches even subtle regressions.
*   **Drawbacks:**
    *   **Brittle:** Sensitive to minor, intentional changes in output format. Requires careful management of snapshots.
    *   **Less Specific:** Doesn't explain *why* something changed, just *that* it changed.

**Example Use Case:** Testing rendering of a React component, JSON API responses, or generated SQL queries.
