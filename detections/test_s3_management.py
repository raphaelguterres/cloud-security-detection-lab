import json
from pathlib import Path
import unittest

from s3_management import PUBLIC_BLOCK_FLAGS, SIGNALS, detect, event_records


ACCOUNT = "000000000000"
BUCKET = "example-fictional-ohio-bucket"


def fixture(name, **overrides):
    return {
        "eventID": f"fixture-{name}",
        "eventTime": "2026-11-24T00:00:00Z",
        "recipientAccountId": ACCOUNT,
        "eventName": name,
        "eventSource": "s3.amazonaws.com",
        "awsRegion": "us-east-2",
        "eventCategory": "Management",
        "readOnly": False,
        "requestParameters": {"bucketName": BUCKET},
        **overrides,
    }


class DetectionTests(unittest.TestCase):
    def scan(self, *events):
        return list(detect(events, ACCOUNT, BUCKET))

    def test_three_successful_management_signals(self):
        results = self.scan(*(fixture(name) for name in SIGNALS))
        self.assertEqual([item["signal"] for item in results], list(SIGNALS.values()))
        self.assertNotIn(ACCOUNT, json.dumps(results))
        self.assertNotIn(BUCKET, json.dumps(results))

    def test_public_access_block_severity(self):
        flags = {key: True for key in PUBLIC_BLOCK_FLAGS}
        params = {"bucketName": BUCKET, "PublicAccessBlockConfiguration": flags}
        event = fixture("PutBucketPublicAccessBlock", requestParameters=params)
        self.assertEqual(self.scan(event)[0]["severity"], "info")
        flags["restrictPublicBuckets"] = False
        self.assertEqual(self.scan(event)[0]["severity"], "high")
        flags.clear()
        self.assertEqual(self.scan(event)[0]["severity"], "review")

    def test_negative_controls(self):
        for overrides in (
            {"awsRegion": "us-east-1"},
            {"recipientAccountId": "111111111111"},
            {"requestParameters": {"bucketName": "other-bucket"}},
            {"eventSource": "ec2.amazonaws.com"},
            {"errorCode": "AccessDenied"},
            {"readOnly": True},
            {"eventCategory": "Data"},
            {"eventID": ""},
        ):
            with self.subTest(overrides=overrides):
                self.assertEqual(self.scan(fixture("PutBucketPolicy", **overrides)), [])
        self.assertEqual(self.scan(fixture("GetObject")), [])

    def test_deduplicate_one_event_id(self):
        event = fixture("DeleteBucket")
        self.assertEqual(len(self.scan(event, event.copy())), 1)

    def test_collect_record_export_formats(self):
        event = fixture("PutBucketPolicy")
        for payload in (event, [event], {"Records": [event]},
                        {"Events": [{"CloudTrailEvent": json.dumps(event)}]}):
            with self.subTest(payload_type=type(payload)):
                self.assertEqual(event_records(payload), [event])

    def test_sanitized_ohio_event_history(self):
        path = Path(__file__).parent / "fixtures" / "ohio-s3-management-sanitized.json"
        events = json.loads(path.read_text(encoding="utf-8"))
        results = list(detect(event_records(events), ACCOUNT, "example-ohio-bucket"))
        self.assertEqual(
            [(item["event"], item["severity"]) for item in results],
            [("PutBucketPublicAccessBlock", "info"), ("PutBucketPolicy", "review"),
             ("DeleteBucket", "review")],
        )


if __name__ == "__main__":
    unittest.main()
