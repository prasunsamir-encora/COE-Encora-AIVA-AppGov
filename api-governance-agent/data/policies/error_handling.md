# Error Handling Policies

- **Rule 3.1:** Use standard HTTP status codes to indicate the outcome of an API request.
- **Rule 3.2:** Successful responses should use `2xx` codes. Client errors should use `4xx` codes. Server errors should use `5xx` codes.
- **Rule 3.3:** Error responses must include a consistent, structured JSON body with a unique error code and a human-readable message, e.g., `{ "error_code": "invalid_parameter", "message": "The 'user_id' parameter is not a valid UUID." }`.
- **Rule 3.4:** Do not expose sensitive information, like stack traces, in error responses.
