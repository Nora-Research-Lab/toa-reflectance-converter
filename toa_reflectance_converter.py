import math

# E_sun values (in W/m²/µm) for common bands (approximate, based on literature)
# Landsat 8 OLI: bands 1-7 (coastal, blue, green, red, NIR, SWIR1, SWIR2)
# Sentinel-2 MSI: bands 2 (blue), 3 (green), 4 (red), 8 (NIR)
_ESUN_TABLE = {
    "Landsat 8 OLI Band 1 (Coastal)": 329.0,
    "Landsat 8 OLI Band 2 (Blue)": 345.0,
    "Landsat 8 OLI Band 3 (Green)": 389.0,
    "Landsat 8 OLI Band 4 (Red)": 318.0,
    "Landsat 8 OLI Band 5 (NIR)": 290.0,
    "Landsat 8 OLI Band 6 (SWIR 1)": 232.0,
    "Landsat 8 OLI Band 7 (SWIR 2)": 95.0,
    "Sentinel-2 MSI Band 2 (Blue)": 348.0,
    "Sentinel-2 MSI Band 3 (Green)": 370.0,
    "Sentinel-2 MSI Band 4 (Red)": 315.0,
    "Sentinel-2 MSI Band 8 (NIR)": 340.0,
}

def get_band_names():
    """Return list of available band names."""
    return list(_ESUN_TABLE.keys())

def get_esun_for_band(band_name):
    """Return E_sun (W/m²/µm) for a given band name, or None if unknown."""
    return _ESUN_TABLE.get(band_name)

def compute_toa_radiance(dn, gain, offset):
    """
    Compute at-sensor radiance L = gain * DN + offset.
    Inputs:
        dn: digital number (non-negative integer, typical 0–65535)
        gain: calibration gain (DN per radiance unit)
        offset: calibration offset
    Returns:
        L: at-sensor radiance (W/m²/sr/µm)
    Raises ValueError on invalid input.
    """
    if dn is None or gain is None or offset is None:
        raise ValueError("All inputs must be provided.")
    try:
        dn = float(dn)
        gain = float(gain)
        offset = float(offset)
    except (TypeError, ValueError):
        raise ValueError("DN, gain, and offset must be numeric.")
    if dn < 0:
        raise ValueError("DN must be non-negative.")
    return gain * dn + offset

def compute_toa_reflectance(L, d, esun, theta_deg):
    """
    Compute TOA reflectance: ρ = (π * L * d^2) / (E_sun * cos(θ * π/180))
    Inputs:
        L: at-sensor radiance (W/m²/sr/µm)
        d: Earth-Sun distance (AU)
        esun: solar exoatmospheric irradiance (W/m²/µm)
        theta_deg: solar zenith angle (degrees, 0-90)
    Returns:
        rho: TOA reflectance (unitless)
    Raises ValueError on invalid input.
    """
    if L is None or d is None or esun is None or theta_deg is None:
        raise ValueError("All inputs must be provided.")
    try:
        L = float(L)
        d = float(d)
        esun = float(esun)
        theta_deg = float(theta_deg)
    except (TypeError, ValueError):
        raise ValueError("All input values must be numeric.")
    if d <= 0:
        raise ValueError("Earth-Sun distance must be positive.")
    if esun <= 0:
        raise ValueError("E_sun must be positive.")
    if theta_deg < 0 or theta_deg > 90:
        raise ValueError("Solar zenith angle must be between 0 and 90 degrees.")
    cos_theta = math.cos(math.radians(theta_deg))
    if cos_theta <= 0:
        return float('nan')  # sun below horizon, geometric limit
    return (math.pi * L * d**2) / (esun * cos_theta)

def classify_reflectance(rho):
    """
    Return a classification string based on reflectance value.
    """
    if rho is None or math.isnan(rho):
        return "Invalid reflectance (NaN). Check inputs."
    if rho < 0:
        return "Negative reflectance – check inputs or solar geometry"
    if rho > 1:
        return "Reflectance > 1 (highly reflective target or calibration issue)"
    return "Reflectance within typical range"
