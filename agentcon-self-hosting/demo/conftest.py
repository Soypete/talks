"""Make the agentware source importable. Point AGENTWARE_SRC at <agentware checkout>/python/src."""

import os
import sys

DEFAULT = os.path.expanduser("~/code/haikei/Agentware/python/src")
sys.path.insert(0, os.environ.get("AGENTWARE_SRC", DEFAULT))

# The analytics scenario reads a private YouTube Studio export (data/*.csv, not committed).
# Without it, skip the tests that need it instead of failing.
collect_ignore = [] if os.path.exists(os.path.join(os.path.dirname(__file__), "data", "videos.csv")) else [
    "tests/data_test.py",
    "tests/workflow_test.py",
]
