# FLIR CSQ / FFF Format Specification

This document records the current understanding of the FLIR CSQ container format used by OpenTRS.

---

# Current Decode Pipeline

```text
CSQ File
    ↓
FFF/RTP Block
    ↓
JPEG-LS Thermal Image
    ↓
RawFrame (uint16)
    ↓
Radiometric Conversion (future)
    ↓
Temperature Frame
```

---

# FFF/RTP Block Signature

## Hex

```text
46 46 46 00 52 54 50 00
```

## ASCII

```text
FFF\0RTP\0
```

## Python

```python
FFF_SIGNATURE = b"FFF\x00RTP\x00"
```

## Description

This byte sequence marks the beginning of a FLIR FFF/RTP block.

OpenTRS searches for this signature to locate every thermal frame stored inside a CSQ file.

---

# JPEG-LS Signatures

## Start Marker

### Hex

```text
FF D8 FF F7
```

### Python

```python
JPEG_LS_SIGNATURE = b"\xff\xd8\xff\xf7"
```

### Description

Marks the beginning of an embedded JPEG-LS thermal image.

---

## End Marker

### Hex

```text
FF D9
```

### Python

```python
JPEG_END_SIGNATURE = b"\xff\xd9"
```

### Description

Marks the end of the embedded JPEG-LS image.

OpenTRS extracts all bytes between the start and end markers before decoding.

---

# Current Implementation

OpenTRS currently performs the following steps:

1. Locate every FFF/RTP block.
2. Locate the embedded JPEG-LS image.
3. Decode JPEG-LS into a 16-bit RawFrame.
4. Store raw sensor values without any radiometric conversion.

---

# Metadata Goals

The following metadata fields still need to be identified and parsed.

| Field | Status |
|--------|--------|
| Image Width | ⏳ |
| Image Height | ⏳ |
| Emissivity | ⏳ |
| Object Distance | ⏳ |
| Reflected Apparent Temperature | ⏳ |
| Atmospheric Temperature | ⏳ |
| Relative Humidity | ⏳ |
| Planck R1 | ⏳ |
| Planck R2 | ⏳ |
| Planck B | ⏳ |
| Planck F | ⏳ |
| Planck O | ⏳ |

---

# Current Limitations

At this stage, image width and height are inferred from the decoded JPEG-LS byte count.

This is a temporary solution.

The long-term goal is to obtain image dimensions directly from FLIR metadata instead of inferring them after decoding.

---

# Future Work

- Parse FLIR metadata records.
- Decode radiometric calibration constants.
- Convert raw sensor values into temperature.
- Support multiple FLIR camera models.
- Fully document the CSQ/FFF file format.