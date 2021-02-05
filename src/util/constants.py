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
