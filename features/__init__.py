"""
Feature modules for Comsol Project Manager
"""
from .quick_run import QuickRunFeature
from .launcher_generator import LauncherGenerator
from .advanced_mode import AdvancedModeFeature
from .inspect_mode import InspectModeFeature

__all__ = [
    'QuickRunFeature',
    'LauncherGenerator',
    'AdvancedModeFeature',
    'InspectModeFeature'
]
