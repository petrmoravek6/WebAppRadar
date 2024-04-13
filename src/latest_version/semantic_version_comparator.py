from typing import Iterable, Optional
from packaging.version import Version, parse
from src.latest_version.cycle_info import CycleInfo
import logging

from src.latest_version.version_comparison import VersionComparison
from src.latest_version.verson_comparator import IVersionComparator

logger = logging.getLogger(__name__)


class SemanticVersionComparator(IVersionComparator):
    @staticmethod
    def _get_latest_version(ver_cycles: Iterable[CycleInfo]) -> Optional[str]:
        try:
            ver_cycle_w_latest_ver = max(ver_cycles, key=lambda v: Version(v.latest), default=None)
            return ver_cycle_w_latest_ver.latest
        except Exception as e:
            logger.error(f'Could not retrieve latest version from found releases: {str(ver_cycles)}. {e}')
            return None

    @staticmethod
    def _get_matching_cycle(curr_version: str, ver_cycles: Iterable[CycleInfo]) -> Optional[CycleInfo]:
        try:
            curr_version_parsed = parse(curr_version)
            curr_major_minor = (curr_version_parsed.major, curr_version_parsed.minor)

            for ver_cycle in ver_cycles:
                ver_cycle_cycle = parse(ver_cycle.cycle)
                major_minor = (ver_cycle_cycle.major, ver_cycle_cycle.minor)

                if major_minor == curr_major_minor:
                    return ver_cycle
            # no cycle matched
            return None
        except Exception as e:
            logger.error(
                f'Could not match current version "{curr_version}" with found releases: {str(ver_cycles)}. {e}')
            return None

    def get_version_comparison(self, curr_version: str, ver_cycles: Iterable[CycleInfo]) -> VersionComparison:
        latest_version = SemanticVersionComparator._get_latest_version(ver_cycles)

        # Only latest version can be discovered if current version is unknown
        if curr_version is None:
            return VersionComparison(latest_version, None, None, None)

        matching_ver_cycle = SemanticVersionComparator._get_matching_cycle(curr_version, ver_cycles)
        if matching_ver_cycle:
            return VersionComparison(latest_version, matching_ver_cycle.latest, matching_ver_cycle.eol,
                                     matching_ver_cycle.eol_date)
        else:
            return VersionComparison(latest_version, None, None, None)
