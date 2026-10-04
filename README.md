![NORA logo](https://i.ibb.co/0VJCC9Gf/IMG-20260114-WA0008.jpg)
 
# TOA Reflectance Converter
 
*For remote sensing analysts and image processors: enter calibration coefficients and a single DN value to instantly compute top-of-atmosphere radiance and reflectance, with band-specific solar irradiance lookup.*
 
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
 

## Overview
 
**Industry:** Remote Sensing & Earth Observation
 
Functional spec for a simple tool that converts a single pixel's digital number (DN) to top-of-atmosphere (TOA) radiance and reflectance for an optical satellite sensor (e.g., Landsat 8/9 OLI, Sentinel-2 MSI). Inputs: (1) Band-specific calibration gain (in DN per radiance unit, e.g., 0.0000271) – number input with unit label; (2) Calibration offset – number input; (3) Digital Number (DN) – integer input (0–65535); (4) Solar zenith angle (θ) in degrees – number input, 0–90; (5) Earth–Sun distance (d) in AU – number input with default of 1.0 (optional override). The tool includes a small lookup table for band-specific solar exoatmospheric irradiance (E_sun) for common satellite bands (Landsat 8 OLI bands 1–7, Sentinel-2 MSI bands 2–4, 8) selectable via a dropdown, or user can manually enter E_sun in W/m²/μm. Core calculation steps: (a) Compute at-sensor radiance: L = gain × DN + offset (units: W/m²/sr/μm). (b) Compute TOA reflectance: ρ = (π × L × d²) / (E_sun × cos(θ × π/180)). The result is a unitless reflectance value typically between 0 and 1 (but can exceed 1 for bright targets). Outputs: two numeric values displayed with 6 significant figures: L_radiance (with unit) and ρ_reflectance (unitless). Additionally, a simple classification flag: if ρ < 0, output 'Negative reflectance – check inputs or solar geometry'; if ρ > 1, output 'Reflectance > 1 (highly reflective target or calibration issue)'; else output 'Reflectance within typical range'. UI: Gradio interface with number inputs, dropdown for band selection (or custom E_sun), and a 'Compute' button. Output shown in two read-only text boxes plus a text label for the classification. No charts or file downloads needed. No AI/ML component – purely deterministic calculation. Layout: two columns: left inputs, right outputs.
 
## Run it
 
```bash
docker build -t toa-reflectance-converter .
docker run -p 7860:7860 toa-reflectance-converter
```
 
Then open http://localhost:7860 in your browser.
 
## About
 
This tool was generated and published automatically by the **NORA Earth Intelligence**
tool factory, an autonomous pipeline maintained by **NORA Research Lab** that turns
one idea per run into a small, working geoscience tool — end to end, with an
LLM writing and Docker-testing the code, and another model generating the
banner above.
 
- Platform: [https://noraearth.xyz](https://noraearth.xyz)
- Parent lab: [https://noraresearchlab.site](https://noraresearchlab.site)
 
Built 2026-10-04.
 
---
 
### Maintainer
 
**NORA Research Lab**
[![GitHub](https://img.shields.io/badge/GitHub-Nora--Research--Lab-181717?logo=github)](https://github.com/Nora-Research-Lab) [![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-NoraResearchLab-yellow)](https://huggingface.co/NoraResearchLab) [![LinkedIn](https://img.shields.io/badge/LinkedIn-NORA%20Research%20Lab-0A66C2?logo=linkedin)](https://www.linkedin.com/company/nora-research-lab) [![X](https://img.shields.io/badge/X-@noraresearchlab-000000?logo=x)](https://x.com/noraresearchlab) [![NORA Research Lab](https://img.shields.io/badge/Website-noraresearchlab.site-2ea44f)](https://noraresearchlab.site) [![NORA Earth Intelligence](https://img.shields.io/badge/Platform-noraearth.xyz-2ea44f)](https://noraearth.xyz)
