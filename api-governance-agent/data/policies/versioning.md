# API Versioning Standards

- **Rule 2.1:** API versions must be included in the URL path, prefixed with 'v', e.g., `/v1/users`.
- **Rule 2.2:** Major version changes (e.g., v1 to v2) indicate breaking changes.
- **Rule 2.3:** Minor and patch version changes should be backward-compatible and can be communicated through response headers, e.g., `API-Version: 1.1.2`.
- **Rule 2.4:** Deprecated endpoints should return a `Warning` header and link to the new endpoint in the response body.
