# Aero-Thermal Reentry Analysis

Synthetic thermal-response study for a generic blunt-body atmospheric entry. It couples a simple exponential atmosphere with convective-heating and lumped thermal-mass models.

## Features

- Altitude-dependent density
- Configurable nose radius and ballistic coefficient
- Sutton-Graves-style normalized heating proxy (educational scaling only)
- Surface temperature integration with radiative cooling
- Peak heat flux, heat load, and temperature metrics
- CSV/JSON outputs, tests, and CI

```mermaid
flowchart LR
 E[Entry State] --> A[Atmosphere]
 A --> H[Convective Heating Proxy]
 H --> T[Thermal Mass Model]
 T --> M[Peak Flux / Heat Load / Temperature]
```

## Run

```bash
python thermal.py --duration 80 --output artifacts
python -m unittest discover -s tests -v
```

All constants are generic educational values. This is not a certified thermal-protection-system design tool.