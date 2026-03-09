"""Sandbox engine registry."""

from .art.sandbox import ArtSandbox
from .audio.sandbox import AudioSandbox
from .cad.sandbox import CADSandbox
from .chemistry.sandbox import ChemistrySandbox
from .design.sandbox import DesignSandbox
from .electronics.sandbox import ElectronicsSandbox
from .kaplay.sandbox import KaplaySandbox
from .logic.sandbox import LogicSandbox
from .math.sandbox import MathSandbox
from .minetest.sandbox import MinetestSandbox
from .music.sandbox import MusicSandbox
from .narrative.sandbox import NarrativeSandbox
from .science.sandbox import ScienceSandbox
from .snap.sandbox import SnapSandbox

__all__ = [
    "ArtSandbox",
    "AudioSandbox",
    "CADSandbox",
    "ChemistrySandbox",
    "DesignSandbox",
    "ElectronicsSandbox",
    "KaplaySandbox",
    "LogicSandbox",
    "MathSandbox",
    "MinetestSandbox",
    "MusicSandbox",
    "NarrativeSandbox",
    "ScienceSandbox",
    "SnapSandbox",
]
