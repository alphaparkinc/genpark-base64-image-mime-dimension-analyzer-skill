from client import ImageHeaderAnalyzer
import struct

# Create sample PNG header
png = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR' + struct.pack('>II', 640, 480) + b'\x08\x06\x00\x00\x00'
info = ImageHeaderAnalyzer.analyze_bytes(png)
print("Image Header Analysis:", info)
