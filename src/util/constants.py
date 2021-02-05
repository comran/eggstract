import os

# Defines the sample rate used by default, unless a custom rate is provided.
DEFAULT_SAMPLE_RATE = 44100
MAXIMUM_WAVE_SIGNAL_VALUE = 1.0
MINIMUM_WAVE_SIGNAL_VALUE = -MAXIMUM_WAVE_SIGNAL_VALUE

# Defines if we're running a test on the CI tool.
TRAVIS = "TRAVIS" in os.environ and os.environ["TRAVIS"] == "true"
TRAVIS_SKIP_REASON = "Skipping this test on Travis CI"

# Defines the project root.
PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.realpath(__file__)) + "/../..")
DATA_ROOT = f"{PROJECT_ROOT}/data"
LIBRARY_ROOT = f"{DATA_ROOT}/raw/library"
LIBRARY_AUDIO_ROOT = f"{LIBRARY_ROOT}/audio"

# Defines the perceived sounds of different frequency ranges.
FREQUENCY_SPECTRUM_CLASSIFICATIONS = [
    {
        "octave": 1,
        "lower_range_hz": 20,
        "upper_range_hz": 40,
        "center": 32,
        "description": "sub-bass",
        "caution": "rumble",
    },
    {
        "octave": 2,
        "lower_range_hz": 40,
        "upper_range_hz": 80,
        "center": 64,
        "description": "low-bass",
        "caution": "loss of definition",
    },
    {
        "octave": 3,
        "lower_range_hz": 80,
        "upper_range_hz": 160,
        "center": 125,
        "description": "bass",
        "caution": "boom",
    },
    {
        "octave": 4,
        "lower_range_hz": 160,
        "upper_range_hz": 320,
        "center": 250,
        "description": "warmth",
        "caution": "muddy",
    },
    {
        "octave": 5,
        "lower_range_hz": 320,
        "upper_range_hz": 640,
        "center": 500,
        "description": "texture",
        "caution": "honky",
    },
    {
        "octave": 6,
        "lower_range_hz": 640,
        "upper_range_hz": 1250,
        "center": 1000,
        "description": "attack",
        "caution": "nasal",
    },
    {
        "octave": 7,
        "lower_range_hz": 1250,
        "upper_range_hz": 2500,
        "center": 2000,
        "description": "crunch",
        "caution": "gritty",
    },
    {
        "octave": 8,
        "lower_range_hz": 2500,
        "upper_range_hz": 5000,
        "center": 4000,
        "description": "clarity",
        "caution": "fatigue",
    },
    {
        "octave": 9,
        "lower_range_hz": 5000,
        "upper_range_hz": 10000,
        "center": 8000,
        "description": "sizzle",
        "caution": "sibilance",
    },
    {
        "octave": 10,
        "lower_range_hz": 10000,
        "upper_range_hz": 20000,
        "center": 16000,
        "description": "air",
        "caution": "hiss",
    },
]
