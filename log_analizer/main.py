import json
import sys
from analizer.analizer import Analyzer, parse_line, parse_message


def convert_sets(obj):
    if isinstance(obj, dict):
        return {k: convert_sets(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_sets(i) for i in obj]
    elif isinstance(obj, set):
        return list(obj)
    else:
        return obj

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <log_file_path>")
        sys.exit(1)
    log_file_path = sys.argv[1]

    analyzer = Analyzer()

    with open(log_file_path, "r") as f:
        for line in f:
            parsed = parse_line(line)
            if not parsed:
                continue

            data = parse_message(parsed)
            analyzer.process(data)

    analyzer.finalize()

    # Convert sets to list for JSON serialization
    block_summary = {
        k: {
            **v,
            "sources": list(v["sources"])
        }
        for k, v in analyzer.block_tracker.items()
    }

    result = {
        "summary": {
            "total_lines": analyzer.total_lines,
            "levels": dict(analyzer.level_count),
        },
        "top_ips": sorted(
            analyzer.ip_count.items(),
            key=lambda x: -x[1]
        )[:10],
        "blocks": dict(list(block_summary.items())[:10]),  # limit output
        "anomalies": analyzer.anomalies[:20]  # limit output
    }

    print(json.dumps(convert_sets(result), indent=2))


if __name__ == "__main__":
    main()
