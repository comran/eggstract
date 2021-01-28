import hashlib
import mmap

EMPTY_STRING_SHA256_HASH = "01ba4719c80b6fe911b091a7c05124b64eeece964e09c058ef8f9805daca546b"


def get_file_sha256(file_path):
    h = hashlib.sha256()

    with open(file_path, "rb") as f:
        # mmap cannot handle empty files, so handle this as a special case.
        if not f.read(1):
            return EMPTY_STRING_SHA256_HASH

        f.seek(0)

        with mmap.mmap(f.fileno(), 0, prot=mmap.PROT_READ) as mm:
            h.update(mm)

    return h.hexdigest()
