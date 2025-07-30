from __future__ import annotations

from typing import Any, Iterable, Callable, List, Union

from . import SFX

class Wavetable:
    def __init__(self, gen: Iterable[float]) -> None: ...

    @staticmethod
    def from_function(f: Callable[[float], float]) -> Wavetable: ...

    @staticmethod
    def sine() -> Wavetable: ...

    @staticmethod
    def triangle() -> Wavetable: ...

    @staticmethod
    def saw() -> Wavetable: ...

    @staticmethod
    def square(duty_cycle: float = 0.5) -> Wavetable: ...

    def __buffer__(self, flags: int, /) -> memoryview: ...

    def __release_buffer__(self, buffer: memoryview, /) -> None: ...


class SoundBuffer:
    sample_rate: int
    channels: int

    def __init__(self, n_samples: int) -> None: ...

    def __len__(self) -> int: ...

    def __getitem__(self, index: int) -> int: ...

    @property
    def duration(self) -> float: ...

    def save(self, filename: str) -> None: ...

    def get_queue_source(self) -> PygletSource: ...

    def __buffer__(self, flags: int, /) -> memoryview: ...

    def __release_buffer__(self, buffer: memoryview, /) -> None: ...


class CachedSound:
    def __init__(self) -> None: ...

    def _clear(self) -> None: ...

    def _set(self, sound: SoundBuffer) -> None: ...

    def _get(self) -> SoundBuffer: ...

    def _build(self) -> SoundBuffer: ...

    def __buffer__(self, flags: int, /) -> memoryview: ...

    def __release_buffer__(self, buffer: memoryview, /) -> None: ...


class PygletSource:
    video_format: None

    def __init__(self, buf: SoundBuffer) -> None: ...

    @property
    def audio_format(self) -> Any: ...

    def get_audio_data(self, length: int) -> Any: ...


def tone(
    wavetable: Wavetable,
    pitch: float = 440.0,
    attack: int = 4000,
    decay: int = 4000,
    sustain: int = 30000,
    release: int = 20000,
) -> SoundBuffer: ...


def sfx(
    wave_type: int = 0,
    p_base_freq: float = 0.3,
    p_freq_limit: float = 0.0,
    p_freq_ramp: float = 0.0,
    p_freq_dramp: float = 0.0,
    p_duty: float = 0.0,
    p_duty_ramp: float = 0.0,
    p_vib_strength: float = 0.0,
    p_vib_speed: float = 0.0,
    p_vib_delay: float = 0.0,
    p_env_attack: float = 0.0,
    p_env_sustain: float = 0.3,
    p_env_decay: float = 0.4,
    p_env_punch: float = 0.0,
    p_lpf_resonance: float = 0.0,
    p_lpf_freq: float = 1.0,
    p_lpf_ramp: float = 0.0,
    p_hpf_freq: float = 0.0,
    p_hpf_ramp: float = 0.0,
    p_pha_offset: float = 0.0,
    p_pha_ramp: float = 0.0,
    p_repeat_speed: float = 0.0,
    p_arp_speed: float = 0.0,
    p_arp_mod: float = 0.0,
) -> SoundBuffer: ...


def pluck(duration: float, pitch: float, release: float = 0.1) -> SoundBuffer: ...


def chord(sounds: List[Union[SoundBuffer, SFX]], stagger: float = 0.0) -> SoundBuffer: ...

