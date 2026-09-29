"""Base64 Image MIME & Dimension Analyzer.
100% Python Standard Library.
"""

import struct
import base64

class ImageHeaderAnalyzer:
    """Parses dimensions (width, height) and MIME type directly from image headers."""
    @staticmethod
    def analyze_bytes(data: bytes) -> dict:
        if len(data) < 24:
            return {"valid": False, "error": "Data too short"}

        if data.startswith(b'\x89PNG\r\n\x1a\n'):
            w, h = struct.unpack('>II', data[16:24])
            return {"valid": True, "mime": "image/png", "width": w, "height": h, "aspect_ratio": round(w / max(h, 1), 4)}

        if data.startswith(b'GIF87a') or data.startswith(b'GIF89a'):
            w, h = struct.unpack('<HH', data[6:10])
            return {"valid": True, "mime": "image/gif", "width": w, "height": h, "aspect_ratio": round(w / max(h, 1), 4)}

        if data.startswith(b'\xff\xd8'):
            idx = 2
            while idx < len(data) - 8:
                if data[idx] != 0xff:
                    idx += 1
                    continue
                marker = data[idx + 1]
                if marker in (0xc0, 0xc1, 0xc2):
                    h, w = struct.unpack('>HH', data[idx + 5:idx + 9])
                    return {"valid": True, "mime": "image/jpeg", "width": w, "height": h, "aspect_ratio": round(w / max(h, 1), 4)}
                else:
                    length = struct.unpack('>H', data[idx + 2:idx + 4])[0]
                    idx += 2 + length
            return {"valid": True, "mime": "image/jpeg", "width": None, "height": None}

        if data.startswith(b'RIFF') and data[8:12] == b'WEBP':
            if data[12:16] == b'VP8 ':
                w = (data[26] | (data[27] << 8)) & 0x3fff
                h = (data[28] | (data[29] << 8)) & 0x3fff
                return {"valid": True, "mime": "image/webp", "width": w, "height": h, "aspect_ratio": round(w / max(h, 1), 4)}

        return {"valid": False, "error": "Unsupported image format"}

    @classmethod
    def analyze_base64(cls, b64_str: str) -> dict:
        if "," in b64_str:
            b64_str = b64_str.split(",", 1)[1]
        raw = base64.b64decode(b64_str)
        res = cls.analyze_bytes(raw)
        res["byte_size"] = len(raw)
        return res
