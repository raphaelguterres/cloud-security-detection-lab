"""Classify successful S3 management events for one authorized Ohio bucket."""
import argparse
import json
from pathlib import Path


REGION = "us-east-2"
SIGNALS = {
    "PutBucketPolicy": "s3.bucket_policy_changed",
    "PutBucketPublicAccessBlock": "s3.public_access_block_changed",
    "DeleteBucket": "s3.bucket_deleted",
}
PUBLIC_BLOCK_FLAGS = (
    "blockPublicAcls",
    "ignorePublicAcls",
    "blockPublicPolicy",
    "restrictPublicBuckets",
)


def event_records(payload):
    if isinstance(payload, list):
        return payload
    if "Events" in payload:
        return [json.loads(item["CloudTrailEvent"]) for item in payload["Events"]]
    if "Records" in payload:
        return payload["Records"]
    return [payload]


def severity(name, params):
    if name != "PutBucketPublicAccessBlock":
        return "review"
    configuration = params.get("PublicAccessBlockConfiguration", {})
    # CloudTrail exports can vary in capitalization of the configuration fields.
    flags = {key.lower(): value for key, value in configuration.items()}
    values = [flags.get(key.lower()) for key in PUBLIC_BLOCK_FLAGS]
    if any(value is False for value in values):
        return "high"
    return "info" if all(value is True for value in values) else "review"


def detect(events, account_id, bucket):
    seen = set()
    for event in events:
        name = event.get("eventName")
        if (name not in SIGNALS or event.get("eventSource") != "s3.amazonaws.com"
                or event.get("awsRegion") != REGION or event.get("eventCategory") != "Management"
                or event.get("recipientAccountId") != account_id or event.get("readOnly") is not False
                or event.get("errorCode")):
            continue
        params = event.get("requestParameters") or {}
        if params.get("bucketName") != bucket:
            continue
        event_id = event.get("eventID")
        timestamp = event.get("eventTime")
        if not event_id or not timestamp or event_id in seen:
            continue
        seen.add(event_id)
        yield {"signal": SIGNALS[name], "event": name, "time_utc": timestamp,
               "region": REGION, "severity": severity(name, params)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("events", type=Path, help="CloudTrail JSON export")
    parser.add_argument("--account-id", required=True)
    parser.add_argument("--bucket", required=True)
    args = parser.parse_args()
    payload = json.loads(args.events.read_text(encoding="utf-8-sig"))
    print(json.dumps(list(detect(event_records(payload), args.account_id, args.bucket)), indent=2))


if __name__ == "__main__":
    main()
