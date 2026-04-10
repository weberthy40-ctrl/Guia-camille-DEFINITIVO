from __future__ import annotations

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from utils.integrity import build_packaging_hygiene_report, write_json  # noqa: E402

REPORT_FILE = BASE_DIR / "data" / "meta" / "packaging_hygiene_report.json"


def main() -> int:
    report = build_packaging_hygiene_report()
    write_json(REPORT_FILE, report)
    if report["clean_for_packaging"]:
        print(f"Packaging hygiene ok. Report written to {REPORT_FILE}")
        if report["removed_noise_items"]:
            print("Removed packaging noise:")
            for item in report["removed_noise_items"]:
                print(f" - {item}")
        return 0

    print(f"Packaging hygiene issues found. Report written to {REPORT_FILE}")
    if report["removed_noise_items"]:
        print("Removed packaging noise before final scan:")
        for item in report["removed_noise_items"]:
            print(f" - {item}")
    for item in report["noise_items_found"]:
        print(f" - {item}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
