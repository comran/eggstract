import pytest
from tempfile import NamedTemporaryFile

from src.util import crypto

@pytest.mark.parametrize("file_data, expected_hash",
    [
        ("", "01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b"),
        ("hello world", "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"),
        ("!thisisatest?@_", "7d87b9e10312ab952c28780d042eda6b276ca0cc45011af74dbe8a6624f91e99")
    ]
)
def test_get_file_sha256(file_data, expected_hash):
    with NamedTemporaryFile() as tmp:
        tmp.write(str.encode(file_data))
        tmp.flush()

        file_hash = crypto.get_file_sha256(tmp.name)
        assert file_hash == expected_hash
