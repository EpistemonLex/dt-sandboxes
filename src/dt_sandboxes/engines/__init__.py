"""Sandbox engine registry."""

from .cad.sandbox import CADSandbox
from .chemistry.sandbox import ChemistrySandbox
from .design.sandbox import DesignSandbox
from .kaplay.sandbox import KaplaySandbox
from .minetest.sandbox import MinetestSandbox
from .music.sandbox import MusicSandbox
from .snap.sandbox import SnapSandbox

__all__ = [
    "CADSandbox",
    "ChemistrySandbox",
    "DesignSandbox",
    "KaplaySandbox",
    "MinetestSandbox",
    "MusicSandbox",
    "SnapSandbox",
]
