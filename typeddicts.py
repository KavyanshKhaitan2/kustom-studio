from typing import TypedDict, Any

class KWGTPresetInfo(TypedDict):
    version: float
    title: str
    description: str
    author: str
    email: str
    width: float
    height: float
    features: str
    release: int
    locked: bool
    pflags: int

class _KWGTPresetRoot(TypedDict):
    internal_events: dict[str, str]
    internal_type: str
    config_scale_value: float
    viewgroup_items: list[dict]

class KWGTPreset(TypedDict):
    preset_info: KWGTPresetInfo
    preset_root: _KWGTPresetRoot