# Hatch build hook – executed automatically when running `uv build`
# # This hook generates stub files for the constants.py module.
import subprocess
import sys
from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface
from hatchling.plugin import hookimpl


class StubGenHook(BuildHookInterface):
    def initialize(self, version, build_data):
        gen = Path(__file__).with_name("gen_stubs.py")
        # python /path/to/gen_stubs.py
        subprocess.check_call([sys.executable, str(gen)])


@hookimpl
def hatch_register_build_hook():
    return StubGenHook
