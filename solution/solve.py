import json
import re
from collections import Counter
from pathlib import Path


LOG_PATH = Path("/app/access.log")
REPORT_PATH = Path("/app/report.json")
REQUEST_PATTERN = re.compile(r'"[A-Z]+\s+(\S+)\s+HTTP/[^\"]+"')


def build_report(log_path: Path) -> dict[str, int | str]:
    paths: Counter[str] = Counter()
    client_ips: set[str] = set()
    total_requests = 0

    with log_path.open(encoding="utf-8") as log_file:
        for raw_line in log_file:
            line = raw_line.strip()
            if not line:
                continue

            match = REQUEST_PATTERN.search(line)
            if match is None:
                raise ValueError(f"Malformed access-log record: {line!r}")

            total_requests += 1
            client_ips.add(line.split(maxsplit=1)[0])
            paths[match.group(1)] += 1

    if not paths:
        raise ValueError("The access log contains no request records")

    return {
        "total_requests": total_requests,
        "unique_ips": len(client_ips),
        "top_path": paths.most_common(1)[0][0],
    }


REPORT_PATH.write_text(
    json.dumps(build_report(LOG_PATH), indent=2) + "\n",
    encoding="utf-8",
)
