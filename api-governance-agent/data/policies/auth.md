# Authentication & Authorization Rules

- **Rule 1.1:** All API endpoints must be protected by OAuth 2.0.
- **Rule 1.2:** The `client_credentials` grant type should be used for machine-to-machine communication.
- **Rule 1.3:** Scopes must be clearly defined for each endpoint to enforce the principle of least privilege.
- **Rule 1.4:** API keys should not be transmitted as query parameters. They must be included in the request header, e.g., `Authorization: Bearer <token>`.
