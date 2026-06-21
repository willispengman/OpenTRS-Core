# OpenTRS Golden Dataset

This directory contains reference CSQ files used for integration testing and reverse engineering.

## Goals

The dataset serves two purposes:

1. Verify decoder correctness.
2. Validate reverse-engineered metadata.

## Naming Convention

```
<camera>_<scene>.csq
```

Examples:

```
flir_e8_room20c.csq
flir_e8_outdoor.csq
flir_t540_metal.csq
```

## Companion Metadata

Each CSQ file may have a companion JSON file.

Example:

```
flir_e8_room20c.csq
flir_e8_room20c.json
```

Example JSON:

```json
{
    "camera": "FLIR E8",
    "resolution": [384, 288],
    "emissivity": 0.98,
    "object_distance_m": 2.0,
    "ambient_temperature_c": 20.0,
    "reflected_temperature_c": 25.0
}
```

The JSON file represents the expected values used for validation.

## Current Dataset

```
sample.csq
```

This sample is currently used for development and reverse engineering.