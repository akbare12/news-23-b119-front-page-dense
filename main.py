"""news-23 b119 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Never writes next to itself: it writes only to
MAKEFUN_OUTPUT_DIR, so it also works from a read-only copy (with
MAKEFUN_OUTPUT_DIR pointed elsewhere). Validates the PNG by parsing its
header and chunk structure with struct/zlib before copying.
"""
import hashlib
import os
import struct
import sys
import zlib

SRC_NAME = "entry.png"
MIN_BYTES = 10_000
MAX_BYTES = 1_048_576


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    return 1


def parse_png(data):
    """Validate PNG structure; return (width, height) or raise ValueError."""
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("bad PNG signature")
    if len(data) < 8 + 25:
        raise ValueError("file too short for IHDR")
    # First chunk must be IHDR, 13 bytes: w, h, bit depth, colour type,
    # compression, filter, interlace.
    (length,) = struct.unpack(">I", data[8:12])
    if data[12:16] != b"IHDR" or length != 13:
        raise ValueError("first chunk is not a 13-byte IHDR")
    w, h, depth, ctype, comp, filt, inter = struct.unpack(">IIBBBBB", data[16:29])
    if (w, h) != (1024, 1024):
        raise ValueError("expected 1024x1024, got %dx%d" % (w, h))
    if depth != 8 or ctype not in (2, 6):
        raise ValueError("expected 8-bit RGB/RGBA, got depth %d type %d" % (depth, ctype))
    if comp != 0 or filt != 0 or inter != 0:
        raise ValueError("unsupported compression/filter/interlace flags")
    ihdr_crc = struct.unpack(">I", data[29:33])[0]
    if zlib.crc32(b"IHDR" + data[16:29]) & 0xFFFFFFFF != ihdr_crc:
        raise ValueError("IHDR CRC mismatch")
    # Walk the remaining chunks, checking CRCs; require a non-empty IDAT
    # payload and a final 0-byte IEND with nothing trailing it.
    # Chunk layout: 4-byte length + 4-byte type + <length> bytes data +
    # 4-byte CRC = 12 bytes overhead. pos starts right after the IHDR
    # chunk: 8 (signature) + 4 (length) + 4 (type) + 13 (IHDR data) + 4 (CRC).
    pos = 8 + 4 + 4 + 13 + 4
    idat_bytes = 0
    seen_iend = False
    while pos < len(data):
        if pos + 8 > len(data):
            raise ValueError("truncated chunk header")
        (clen,) = struct.unpack(">I", data[pos:pos + 4])
        ctype_b = data[pos + 4:pos + 8]
        if pos + 12 + clen > len(data):
            raise ValueError("truncated chunk " + ctype_b.decode("latin1"))
        crc = struct.unpack(">I", data[pos + 8 + clen:pos + 12 + clen])[0]
        if zlib.crc32(ctype_b + data[pos + 8:pos + 8 + clen]) & 0xFFFFFFFF != crc:
            raise ValueError("CRC mismatch in chunk " + ctype_b.decode("latin1"))
        if ctype_b == b"IDAT":
            if clen == 0:
                raise ValueError("empty IDAT chunk")
            idat_bytes += clen
        if ctype_b == b"IEND":
            if clen != 0:
                raise ValueError("IEND must be 0 bytes")
            if pos + 12 != len(data):
                raise ValueError("trailing data after IEND")
            seen_iend = True
            break
        pos += 12 + clen
    if not seen_iend:
        raise ValueError("missing IEND chunk")
    if idat_bytes < 1000:
        raise ValueError("IDAT payload too small (%d bytes)" % idat_bytes)
    return w, h


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, SRC_NAME)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        return fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir = os.path.abspath(out_dir)
    if out_dir == here or out_dir.startswith(here + os.sep):
        return fail("MAKEFUN_OUTPUT_DIR must not be inside the repo")
    if os.path.exists(out_dir) and not os.path.isdir(out_dir):
        return fail("MAKEFUN_OUTPUT_DIR exists and is not a directory")
    dst = os.path.join(out_dir, SRC_NAME)
    if os.path.abspath(dst) == src:
        return fail("output would overwrite the source image")
    if not os.path.isfile(src):
        return fail("source image not found: " + src)
    with open(src, "rb") as f:
        data = f.read()
    if len(data) < MIN_BYTES:
        return fail("source image too small (%d bytes)" % len(data))
    if len(data) > MAX_BYTES:
        return fail("source image over 1 MiB (%d bytes)" % len(data))
    try:
        w, h = parse_png(data)
    except ValueError as e:
        return fail(str(e))
    os.makedirs(out_dir, exist_ok=True)
    with open(dst, "wb") as f:
        f.write(data)
    with open(dst, "rb") as f:
        written = f.read()
    if written != data:
        return fail("re-read of output does not match source")
    print("wrote %s (%dx%d, %d bytes, sha256 %s)"
          % (dst, w, h, len(data), hashlib.sha256(data).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
