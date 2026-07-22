Analyze the Apache-style access log at `/app/access.log` and write a summary to
`/app/report.json`.

The task is complete when:

1. `/app/report.json` is valid JSON containing exactly the keys `total_requests`,
   `unique_ips`, and `top_path`. The first two values are integers and `top_path`
   is a string.
2. `total_requests` is the number of non-empty request records in the access log.
3. `unique_ips` is the number of distinct client IP addresses in those records.
4. `top_path` is the request path that occurs most often in the log.
