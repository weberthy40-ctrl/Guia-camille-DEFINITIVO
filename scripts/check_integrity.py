from __future__ import annotations

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from utils.integrity import build_learning_integrity_report, build_merge_readiness_report, build_packaging_hygiene_report, write_json  # noqa: E402

META_DIR = BASE_DIR / "data" / "meta"
LEARNING_REPORT_FILE = META_DIR / "learning_integrity_report.json"
MERGE_REPORT_FILE = META_DIR / "merge_readiness_report.json"
PACKAGING_REPORT_FILE = META_DIR / "packaging_hygiene_report.json"



def main() -> None:
    learning_report = build_learning_integrity_report()
    packaging_report = build_packaging_hygiene_report()
    merge_report = build_merge_readiness_report(packaging_report=packaging_report)

    write_json(LEARNING_REPORT_FILE, learning_report)
    write_json(PACKAGING_REPORT_FILE, packaging_report)
    write_json(MERGE_REPORT_FILE, merge_report)

    print(f"Learning integrity report written to {LEARNING_REPORT_FILE}")
    print(f"Packaging hygiene report written to {PACKAGING_REPORT_FILE}")
    print(f"Merge readiness report written to {MERGE_REPORT_FILE}")
    if merge_report["ready_for_parallel_merge_prep"]:
        print("Principal line is ready for future approved-package merge prep.")
    else:
        print("Principal line still has warnings before future merge prep.")
        if merge_report["missing_required_runtime_files"]:
            print("Missing required runtime files:")
            for item in merge_report["missing_required_runtime_files"]:
                print(f" - {item}")
        if merge_report["missing_required_docs"]:
            print("Missing required docs:")
            for item in merge_report["missing_required_docs"]:
                print(f" - {item}")
        if merge_report["missing_meta_outputs"]:
            print("Missing meta outputs:")
            for item in merge_report["missing_meta_outputs"]:
                print(f" - {item}")
        if not merge_report["packaging"]["clean_for_packaging"]:
            print("Packaging noise detected:")
            for item in merge_report["packaging"]["noise_items_found"]:
                print(f" - {item}")


if __name__ == "__main__":
    main()
