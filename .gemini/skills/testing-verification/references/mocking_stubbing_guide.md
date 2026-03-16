# Mocking and Stubbing Guide

Mocking and stubbing are essential techniques in software testing, particularly for unit and integration tests. They allow you to isolate the component being tested from its dependencies, making tests faster, more reliable, and easier to write.

## Why Mock/Stub?

*   **Isolation:** Test a single unit of code without interference from its collaborators.
*   **Speed:** Avoid slow operations like database calls, network requests, or file I/O.
*   **Determinism:** Ensure tests produce the same results every time, regardless of external system states.
*   **Control:** Simulate complex scenarios or error conditions that are difficult to reproduce with real dependencies.
*   **Test Unimplemented Features:** Test code that relies on components not yet built.

## Key Concepts

### 1. Mock
A mock object is a simulated object that mimics the behavior of real objects in controlled ways. It records calls made to it and allows you to verify that the correct methods were called with the correct arguments. Mocks are often used when you need to verify *interactions* between objects.

**Example Use Case:** Verifying that a `UserService` correctly calls `EmailService.send_welcome_email()` after user registration.

### 2. Stub
A stub is a minimal implementation of an interface or class that provides canned answers to calls made during the test. Stubs do not typically include any assertion or verification logic; they simply return predefined values. Stubs are used when you need to provide *state* to the object under test.

**Example Use Case:** Providing a `DatabaseGateway` stub that always returns a specific user object when `get_user_by_id()` is called.

### 3. Fake
A fake object has working implementations, but usually simplifies the actual behavior. Fakes often take shortcuts and are not suitable for production (e.g., an in-memory database that simulates a real database).

**Example Use Case:** Using an in-memory `FakeRepository` that stores data in a list instead of a real database.

### 4. Spy
A spy is a partial mock or partial stub. It wraps a real object and allows you to record calls made to it or override specific methods while still allowing other methods to behave normally.

**Example Use Case:** Observing how many times a method of a real object was called without fully replacing the object.

## Best Practices

*   **Test Behavior, Not Implementation Details:** Focus on what the code *does*, not *how* it does it. Avoid over-mocking internal details.
*   **Mock/Stub at Boundaries:** Only mock/stub objects at the boundaries of the system you are testing (e.g., external services, databases, file system). Don't mock objects internal to the component under test.
*   **Readability:** Make your mocks/stubs easy to understand. The setup should be clear.
*   **Avoid Over-Mocking:** Too many mocks can make tests brittle and hard to refactor. If a unit test requires excessive mocking, it might indicate that the unit has too many responsibilities or tight coupling.
*   **Choose the Right Tool:**
    *   **Python:** `unittest.mock` module (MagicMock, patch).
    *   **JavaScript/TypeScript:** Jest mocks, Sinon.js.
    *   **Java:** Mockito, EasyMock.
*   **Cleanup:** Always ensure that any mocking or stubbing is properly cleaned up after each test to prevent test pollution. (e.g., `unittest.mock.patch` context managers or decorators).

## Example (Python with `unittest.mock.patch`)

```python
import unittest
from unittest.mock import patch

# Assume this is the code you want to test
class UserService:
    def __init__(self, email_service):
        self.email_service = email_service

    def register_user(self, username, email):
        if not self.email_service.send_welcome_email(email, f"Welcome, {username}!"):
            raise Exception("Failed to send welcome email")
        return {"username": username, "email": email}

# Assume this is a dependency
class EmailService:
    def send_welcome_email(self, recipient, message):
        print(f"Sending email to {recipient}: {message}")
        # In a real app, this would involve network I/O
        return True

class TestUserService(unittest.TestCase):

    @patch('my_module.EmailService') # Patching the EmailService wherever it's imported
    def test_register_user_sends_email(self, MockEmailService):
        # Arrange
        # Configure the mock to return True for send_welcome_email
        MockEmailService.return_value.send_welcome_email.return_value = True
        
        user_service = UserService(MockEmailService.return_value)
        username = "testuser"
        email = "test@example.com"

        # Act
        result = user_service.register_user(username, email)

        # Assert
        self.assertIsNotNone(result)
        # Verify that send_welcome_email was called exactly once with the correct arguments
        MockEmailService.return_value.send_welcome_email.assert_called_once_with(email, f"Welcome, {username}!")

    @patch('my_module.EmailService')
    def test_register_user_raises_exception_on_email_failure(self, MockEmailService):
        # Arrange
        # Configure the mock to return False for send_welcome_email
        MockEmailService.return_value.send_welcome_email.return_value = False
        
        user_service = UserService(MockEmailService.return_value)
        username = "testuser"
        email = "test@example.com"

        # Act & Assert
        with self.assertRaises(Exception) as cm:
            user_service.register_user(username, email)
        self.assertEqual(str(cm.exception), "Failed to send welcome email")
```
(Note: `my_module` would be the actual module where `UserService` and `EmailService` are defined)
