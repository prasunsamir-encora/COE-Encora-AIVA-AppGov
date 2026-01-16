# Authentication & Authorization Rules

- **Rule 1.1:** All API endpoints must be protected by OAuth 2.0.
- **Rule 1.2:** The `client_credentials` grant type should be used for machine-to-machine communication.
- **Rule 1.3:** Scopes must be clearly defined for each endpoint to enforce the principle of least privilege.
- **Rule 1.4:** API keys should not be transmitted as query parameters. They must be included in the request header, e.g., `Authorization: Bearer <token>`.

# Error Handling Policies

- **Rule 3.1:** Use standard HTTP status codes to indicate the outcome of an API request.
- **Rule 3.2:** Successful responses should use `2xx` codes. Client errors should use `4xx` codes. Server errors should use `5xx` codes.
- **Rule 3.3:** Error responses must include a consistent, structured JSON body with a unique error code and a human-readable message, e.g., `{ "error_code": "invalid_parameter", "message": "The 'user_id' parameter is not a valid UUID." }`.
- **Rule 3.4:** Do not expose sensitive information, like stack traces, in error responses.

# Naming Conventions

- **Rule 5.1:** Resource names in URLs should be plural and use kebab-case, e.g., `/purchase-orders`.
- **Rule 5.2:** JSON property names should use snake_case, e.g., `{ "user_id": 123 }`.
- **Rule 5.3:** Query parameters should use snake_case, e.g., `?sort_by=created_at`.
- **Rule 5.4:** Avoid using abbreviations. Favor descriptive names over short ones.

# Rate, Quota, and SLA Policies

- **Rule 6.1:** The default rate limit for authenticated users is 1,000 requests per minute.
- **Rule 6.2:** Exceeding the rate limit should result in a `429 Too Many Requests` error.
- **Rule 6.3:** The `Retry-After` header should be included in `429` responses, indicating how many seconds to wait before making a new request.
- **Rule 6.4:** Different API tiers (e.g., Free, Premium) may have different rate limits and quotas, which must be documented in the API's SLA.

# Security Best Practices

- **Rule 4.1:** All data in transit must be encrypted using TLS 1.2 or higher.
- **Rule 4.2:** Implement input validation to prevent injection attacks (e.g., SQL, NoSQL, command injection).
- **Rule 4.3:** Use a Content Security Policy (CSP) to prevent cross-site scripting (XSS) attacks.
- **Rule 4.4:** Rate limiting must be implemented to protect against denial-of-service (DoS) attacks.
- **Rule 4.5:** APIs must not expose sensitive data in GET requests.

# API Versioning Standards

- **Rule 2.1:** API versions must be included in the URL path, prefixed with 'v', e.g., `/v1/users`.
- **Rule 2.2:** Major version changes (e.g., v1 to v2) indicate breaking changes.
- **Rule 2.3:** Minor and patch version changes should be backward-compatible and can be communicated through response headers, e.g., `API-Version: 1.1.2`.
- **Rule 2.4:** Deprecated endpoints should return a `Warning` header and link to the new endpoint in the response body.
