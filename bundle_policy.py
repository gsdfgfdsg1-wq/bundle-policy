#!/usr/bin/env python3
"""Enforce route, asset type, and third-party bundle budgets."""
import argparse
import json
from pathlib import Path
from urllib.parse import urlparse


def category(asset):
    name = asset["name"].lower()
    if name.endswith(".js"):
        return "script"
    if name.endswith(".css"):
        return "style"
    if name.endswith((".png", ".jpg", ".jpeg", ".webp", ".svg")):
        return "image"
    return "other"


def evaluate(manifest, policy):
    violations, totals = [], {}
    for asset in manifest["assets"]:
        size = asset["bytes"]
        route = asset.get("route", "global")
        kind = category(asset)
        host = urlparse(asset["name"]).netloc
        for key in (f"route:{route}", f"type:{kind}", "total"):
            totals[key] = totals.get(key, 0) + size
        if host:
            totals[f"third-party:{host}"] = totals.get(f"third-party:{host}", 0) + size
    for scope, limit in policy.get("budgets", {}).items():
        actual = totals.get(scope, 0)
        if actual > limit:
            violations.append({"scope": scope, "budget": limit, "actual": actual, "over": actual - limit})
    return {"totals": totals, "violations": violations, "ok": not violations}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", help="JSON with an assets array")
    parser.add_argument("policy", help="JSON with budgets mapping")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args()
    report = evaluate(json.loads(Path(args.manifest).read_text()), json.loads(Path(args.policy).read_text()))
    if args.format == "json":
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print("# Bundle policy report\n\n" + ("PASS" if report["ok"] else "FAIL"))
        for item in report["violations"]:
            print(f"- `{item['scope']}`: {item['actual']} bytes / {item['budget']} bytes")
    raise SystemExit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
