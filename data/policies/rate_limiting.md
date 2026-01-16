# Rate, Quota, and SLA Policies

- **Rule 6.1:** The default rate limit for authenticated users is 1,000 requests per minute.
- **Rule 6.2:** Exceeding the rate limit should result in a `429 Too Many Requests` error.
- **Rule 6.3:** The `Retry-After` header should be included in `429` responses, indicating how many seconds to wait before making a new request.
- **Rule 6.4:** Different API tiers (e.g., Free, Premium) may have different rate limits and quotas, which must be documented in the API's SLA.
