"""Compatibility entry point for the packaged bind-time demonstrator.

The authoritative implementation lives in bind_time_authority_fabric.
"""
from contextlib import redirect_stdout
from io import StringIO

from bind_time_authority_fabric.advanced_execution_field import simulate as _simulate


def simulate(steps: int = 12):
    """Run the packaged demo quietly and return its deterministic hash chain."""
    with redirect_stdout(StringIO()):
        return _simulate(steps=steps)
