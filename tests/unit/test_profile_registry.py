import unittest
from pathlib import Path

from pfem.profile_runtime import load_profile_registry, validate_profile_registry


ROOT = Path(__file__).resolve().parents[2]


class ProfileRegistryTests(unittest.TestCase):
    def test_profile_registry_loads(self):
        registry = load_profile_registry(ROOT / "profiles" / "profile-registry.json")
        self.assertEqual(registry.registry_id, "pfem-profile-registry")
        self.assertGreaterEqual(len(registry.profiles), 1)

    def test_profile_registry_validates(self):
        failures = validate_profile_registry(ROOT)
        self.assertEqual(failures, [])


if __name__ == "__main__":
    unittest.main()
