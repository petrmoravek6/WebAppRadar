import unittest
from datetime import datetime

from src.latest_version.semantic_version_comparator import SemanticVersionComparator
from src.latest_version.verson_comparator import VersionCycleInfo


class TestSemanticVersionComparator(unittest.TestCase):
    def setUp(self):
        self.comparator = SemanticVersionComparator()

    def test_latest_version(self):
        ver_cycles1 = [
            VersionCycleInfo(cycle='1.0', latest='1.0.5', eol=False, eol_date=None),
            VersionCycleInfo(cycle='2.0', latest='2.0.3', eol=False, eol_date=None),
        ]
        ver_cycles2 = [
            VersionCycleInfo(cycle='2024.3', latest='2024.3.2', eol=False, eol_date=None),
            VersionCycleInfo(cycle='2023.9', latest='2023.9', eol=False, eol_date=None),
        ]
        ver_cycles3 = [
            VersionCycleInfo(cycle='2024.3', latest='2024.3', eol=False, eol_date=None),
            VersionCycleInfo(cycle='2023.9', latest='2023.9.11', eol=False, eol_date=None),
        ]

        result1 = self.comparator.get_version_comparison('2.0.1', ver_cycles1)
        result2 = self.comparator.get_version_comparison('1.0.4', ver_cycles1)
        result3 = self.comparator.get_version_comparison('1.0.5', ver_cycles1)
        result4 = self.comparator.get_version_comparison('2.0.3', ver_cycles1)
        result5 = self.comparator.get_version_comparison('0.5.5', ver_cycles1)
        result6 = self.comparator.get_version_comparison('3.0.3', ver_cycles1)
        result7 = self.comparator.get_version_comparison('2.0.99', ver_cycles1)
        result8 = self.comparator.get_version_comparison('1.0', ver_cycles1)
        result9 = self.comparator.get_version_comparison('2.0', ver_cycles1)
        result10 = self.comparator.get_version_comparison('3.0', ver_cycles1)
        result11 = self.comparator.get_version_comparison('2023.1.1', ver_cycles2)
        result12 = self.comparator.get_version_comparison('2023.9', ver_cycles2)
        result13 = self.comparator.get_version_comparison('2024.3.1', ver_cycles2)
        result14 = self.comparator.get_version_comparison('2023.3.1', ver_cycles3)

        self.assertEqual(result1.latest_version, '2.0.3')
        self.assertEqual(result2.latest_version, '2.0.3')
        self.assertEqual(result3.latest_version, '2.0.3')
        self.assertEqual(result4.latest_version, '2.0.3')
        self.assertEqual(result5.latest_version, '2.0.3')
        self.assertEqual(result6.latest_version, '2.0.3')
        self.assertEqual(result7.latest_version, '2.0.3')
        self.assertEqual(result8.latest_version, '2.0.3')
        self.assertEqual(result9.latest_version, '2.0.3')
        self.assertEqual(result10.latest_version, '2.0.3')
        self.assertEqual(result11.latest_version, '2024.3.2')
        self.assertEqual(result12.latest_version, '2024.3.2')
        self.assertEqual(result13.latest_version, '2024.3.2')
        self.assertEqual(result14.latest_version, '2024.3')

    def test_matching_cycle(self):
        ver_cycles1 = [
            VersionCycleInfo(cycle='1.0', latest='1.0.5', eol=True, eol_date=None),
            VersionCycleInfo(cycle='2.0', latest='2.0.3', eol=False, eol_date=None),
        ]
        ver_cycles2 = [
            VersionCycleInfo(cycle='2024.3', latest='2024.3.2', eol=True, eol_date=datetime.now().date()),
            VersionCycleInfo(cycle='2023.9', latest='2023.9', eol=False, eol_date=None),
        ]
        ver_cycles3 = [
            VersionCycleInfo(cycle='2024.3', latest='2024.3', eol=None, eol_date=None),
            VersionCycleInfo(cycle='2023.9', latest='2023.9.11', eol=None, eol_date=None),
        ]

        result1 = self.comparator.get_version_comparison('2.0.1', ver_cycles1)
        result2 = self.comparator.get_version_comparison('1.0.4', ver_cycles1)
        result3 = self.comparator.get_version_comparison('1.0.5', ver_cycles1)
        result4 = self.comparator.get_version_comparison('2.0.3', ver_cycles1)
        result5 = self.comparator.get_version_comparison('0.5.5', ver_cycles1)
        result6 = self.comparator.get_version_comparison('3.0.3', ver_cycles1)
        result7 = self.comparator.get_version_comparison('2.0.99', ver_cycles1)
        result8 = self.comparator.get_version_comparison('1.0', ver_cycles1)
        result9 = self.comparator.get_version_comparison('2.0', ver_cycles1)
        result10 = self.comparator.get_version_comparison('3.0', ver_cycles1)
        result11 = self.comparator.get_version_comparison('2023.1.1', ver_cycles2)
        result12 = self.comparator.get_version_comparison('2023.9', ver_cycles2)
        result13 = self.comparator.get_version_comparison('2024.3.1', ver_cycles2)
        result14 = self.comparator.get_version_comparison('2023.9', ver_cycles3)

        self.assertEqual(result1.latest_cycle_version, '2.0.3')
        self.assertFalse(result1.eol)
        self.assertIsNone(result1.eol_date)
        self.assertEqual(result2.latest_cycle_version, '1.0.5')
        self.assertTrue(result2.eol)
        self.assertIsNone(result2.eol_date)
        self.assertEqual(result3.latest_cycle_version, '1.0.5')
        self.assertTrue(result3.eol)
        self.assertIsNone(result3.eol_date)
        self.assertEqual(result4.latest_cycle_version, '2.0.3')
        self.assertFalse(result4.eol)
        self.assertIsNone(result4.eol_date)
        self.assertIsNone(result5.latest_cycle_version)
        self.assertIsNone(result6.latest_cycle_version)
        self.assertEqual(result7.latest_cycle_version, '2.0.3')
        self.assertFalse(result7.eol)
        self.assertEqual(result8.latest_cycle_version, '1.0.5')
        self.assertTrue(result8.eol)
        self.assertIsNone(result8.eol_date)
        self.assertEqual(result9.latest_cycle_version, '2.0.3')
        self.assertFalse(result9.eol)
        self.assertIsNone(result10.latest_cycle_version)
        self.assertIsNone(result11.latest_cycle_version)
        self.assertEqual(result12.latest_cycle_version, '2023.9')
        self.assertEqual(result13.latest_cycle_version, '2024.3.2')
        self.assertTrue(result13.eol)
        self.assertIsNotNone(result13.eol_date)
        self.assertEqual(result14.latest_cycle_version, '2023.9.11')
        self.assertIsNone(result14.eol_date)
        self.assertIsNone(result14.eol)

    def test_no_versions(self):
        ver_cycles = []

        result = self.comparator.get_version_comparison('1.0.2', ver_cycles)
        self.assertIsNone(result.latest_version)

    def test_invalid_current_version(self):
        ver_cycles = [
            VersionCycleInfo(cycle='1.0', latest='1.0.5', eol=False, eol_date=None),
        ]

        result = self.comparator.get_version_comparison('invalid.version', ver_cycles)

        self.assertEqual(result.latest_version, '1.0.5')
        self.assertIsNone(result.latest_cycle_version)
        self.assertIsNone(result.eol)
        self.assertIsNone(result.eol_date)
