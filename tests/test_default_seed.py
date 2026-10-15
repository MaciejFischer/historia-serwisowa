import datetime
import json
import pathlib
import re
import unittest


SOURCE = pathlib.Path(__file__).parents[1].joinpath("index.html").read_text()


def embedded_seed():
    start = SOURCE.index("var SEED = ") + len("var SEED = ")
    depth = 0
    in_string = False
    escaped = False
    for end in range(start, len(SOURCE)):
        char = SOURCE[end]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
        elif char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return json.loads(SOURCE[start:end + 1])
    raise AssertionError("Embedded SEED object is incomplete")


class DefaultSeedValidation(unittest.TestCase):
    def test_seed_entries_pass_import_normalization_constraints(self):
        seed = embedded_seed()
        entries = seed["entries"]
        self.assertEqual(len(entries), 77)
        ids = set()
        for entry in entries:
            self.assertIsInstance(entry.get("id"), (int, float))
            self.assertNotIsInstance(entry.get("id"), bool)
            self.assertTrue(str(entry["id"]).strip())
            self.assertNotIn(entry["id"], ids)
            ids.add(entry["id"])
            self.assertIsInstance(entry.get("title"), str)
            self.assertTrue(entry["title"].strip())
            self.assertIsInstance(entry.get("category"), str)
            self.assertIn(entry.get("status"), ("completed", "planned"))
            if entry.get("date") is not None:
                self.assertRegex(entry["date"], r"^\d{4}-\d{2}-\d{2}$")
                datetime.date.fromisoformat(entry["date"])
            if entry.get("mileage") is not None:
                self.assertGreaterEqual(float(entry["mileage"]), 0)
            for key in ("mileageApprox", "done"):
                if key in entry:
                    self.assertIsInstance(entry[key], bool)

        planned_ids = {entry["id"] for entry in entries if entry["status"] == "planned"}
        order = seed["plannedOrder"]
        self.assertEqual(len(order), len(set(order)))
        self.assertEqual(set(order), planned_ids)

    def test_fresh_install_and_reset_use_seed_order_without_replacing_saved_data(self):
        self.assertIn("Array.isArray(SEED.plannedOrder)?clone(SEED.plannedOrder)", SOURCE)
        self.assertIn("order=Array.isArray(SEED.plannedOrder)?clone(SEED.plannedOrder)", SOURCE)
        self.assertIn("storedData&&!storedData.error?storedData.entries:clone(SEED.entries)", SOURCE)
        self.assertIn("storedData&&!storedData.error?storedData.order:", SOURCE)
        self.assertRegex(SOURCE, r"var storedEntries=load\(K_ENTRIES,\s*null\)")


if __name__ == "__main__":
    unittest.main()
