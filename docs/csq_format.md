# FLIR CSQ / FFF Format Specification

**Project:** OpenTRS-Core

**Status:** Work in Progress

This document records the current understanding of the FLIR CSQ container format as reverse engineered by the OpenTRS project.

---

# Decode Pipeline

Current decoding pipeline implemented by OpenTRS.

```text
CSQ File
    │
    ▼
FFF/RTP Blocks
    │
    ▼
JPEG-LS Thermal Image
    │
    ▼
16-bit RawFrame
    │
    ▼
Radiometric Conversion (future)
    │
    ▼
Temperature Frame
```

---

# File Structure

Current understanding of one CSQ file.

```text
CSQ

├── FFF Block 0
│     ├── Header / Metadata
│     ├── JPEG-LS
│     └── Trailer
│
├── FFF Block 1
│     ├── Header / Metadata
│     ├── JPEG-LS
│     └── Trailer
│
└── ...
```

---

# Known Signatures

## FFF/RTP Block

### Hex

```text
46 46 46 00 52 54 50 00
```

### ASCII

```text
FFF\0RTP\0
```

### Python

```python
FFF_SIGNATURE = b"FFF\x00RTP\x00"
```

### Description

Marks the beginning of a FLIR FFF/RTP block.

---

## JPEG-LS Start Marker

### Hex

```text
FF D8 FF F7
```

### Python

```python
JPEG_LS_SIGNATURE = b"\xff\xd8\xff\xf7"
```

---

## JPEG-LS End Marker

### Hex

```text
FF D9
```

### Python

```python
JPEG_END_SIGNATURE = b"\xff\xd9"
```

---

# Current Reverse Engineering Results

The following values were observed in `tests/data/sample.csq`.

These observations require verification using additional CSQ files.

| Offset | Type | Value | Confidence | Interpretation |
|--------:|------|------:|------------|----------------|
| 0x0160 | float32 | 0.98 | ★★★★☆ | Likely emissivity |
| 0x0164 | float32 | 2.0 | ★★★☆☆ | Likely object distance (m) |
| 0x0168 | float32 | 298.15 | ★★★☆☆ | Kelvin (≈25°C) |
| 0x016C | float32 | 293.15 | ★★★☆☆ | Kelvin (≈20°C) |
| 0x0170 | float32 | 293.15 | ★★★☆☆ | Kelvin (≈20°C) |
| 0x0174 | float32 | 1.0 | ★★☆☆☆ | Unknown |
| 0x017C | float32 | 0.5 | ★★☆☆☆ | Unknown |
| 0x0180 | float32 | 6.0 | ★★☆☆☆ | Unknown |
| 0x0198 | float32 | 16061.46 | ★★★☆☆ | Possible Planck constant |
| 0x019C | float32 | 1418.90 | ★★★★☆ | Likely Planck B |
| 0x01A0 | float32 | 1.0 | ★★★☆☆ | Possible Planck F |

---

# FFF Block Layout

Current observations.

```text
+----------------------------+
| FFF/RTP Signature          |
+----------------------------+
| Header / Metadata          |
|                            |
| 3796 bytes                 |
|                            |
+----------------------------+
| JPEG-LS                    |
+----------------------------+
| Trailer / Unknown          |
+----------------------------+
```

---

# Known Sample

Current development sample.

| Property | Value |
|----------|------:|
| Blocks | 183 |
| Header Size | 3796 bytes |
| First JPEG Offset | 3796 |
| First JPEG Size | 41371 bytes |
| Resolution | 384 × 288 |

---

# Metadata Targets

The following fields are still under investigation.

| Field | Status |
|-------|--------|
| Camera Model | ⏳ |
| Image Width | 🔄 |
| Image Height | 🔄 |
| Emissivity | 🔄 |
| Object Distance | 🔄 |
| Reflected Temperature | ⏳ |
| Atmospheric Temperature | 🔄 |
| Relative Humidity | ⏳ |
| IR Window Temperature | ⏳ |
| IR Window Transmission | ⏳ |
| Planck R1 | ⏳ |
| Planck R2 | ⏳ |
| Planck B | 🔄 |
| Planck F | 🔄 |
| Planck O | ⏳ |

Legend:

- ✅ Confirmed
- 🔄 Under Investigation
- ⏳ Unknown

---

# Current Limitations

Current image dimensions are inferred after JPEG-LS decoding.

Future versions should obtain image dimensions directly from metadata.

---

# Future Work

- Decode FFF metadata records.
- Identify radiometric calibration constants.
- Convert raw counts into physical temperature.
- Support multiple FLIR camera models.
- Fully document the FLIR CSQ/FFF specification.