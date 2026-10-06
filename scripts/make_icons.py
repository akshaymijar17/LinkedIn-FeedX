#!/usr/bin/env python3
"""Generate the FeedX icons (blue rounded square with a white X).

Pure standard library, no Pillow needed. Run from the repo root:
    python3 scripts/make_icons.py
"""
import struct
import zlib
from pathlib import Path

BLUE = (10, 102, 194)
WHITE = (255, 255, 255)
SUPERSAMPLE = 4


def coverage(size, x, y):
    """Return (in_square, in_x) for a point in [0, size)."""
    radius = size * 0.22
    # Rounded square covering the whole canvas.
    cx = min(max(x, radius), size - radius)
    cy = min(max(y, radius), size - radius)
    in_square = (x - cx) ** 2 + (y - cy) ** 2 <= radius ** 2

    # Two diagonal strokes forming an X, inset from the edges.
    u, v = x / size - 0.5, y / size - 0.5
    half_width = 0.085
    extent = 0.25
    in_x = (abs(u) <= extent and abs(v) <= extent) and (
        abs(u - v) / 2 ** 0.5 <= half_width or abs(u + v) / 2 ** 0.5 <= half_width
    )
    return in_square, in_x


def render(size):
    rows = []
    n = SUPERSAMPLE
    for py in range(size):
        row = bytearray([0])  # PNG filter type: none
        for px in range(size):
            r = g = b = a = 0
            for sy in range(n):
                for sx in range(n):
                    in_square, in_x = coverage(size, px + (sx + 0.5) / n, py + (sy + 0.5) / n)
                    if in_square:
                        color = WHITE if in_x else BLUE
                        r += color[0]; g += color[1]; b += color[2]; a += 255
            samples = n * n
            covered = a // 255
            if covered:
                row += bytes([r // covered, g // covered, b // covered, a // samples])
            else:
                row += bytes(4)
        rows.append(bytes(row))
    return b"".join(rows)


def png(size):
    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data))

    header = struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)
    return (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", header)
        + chunk(b"IDAT", zlib.compress(render(size), 9))
        + chunk(b"IEND", b"")
    )


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "icons"
    out.mkdir(exist_ok=True)
    for size in (16, 48, 128):
        (out / f"icon{size}.png").write_bytes(png(size))
        print(f"wrote icons/icon{size}.png")
