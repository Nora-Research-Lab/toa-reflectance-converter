import gradio as gr
from toa_reflectance_converter import (
    get_band_names,
    get_esun_for_band,
    compute_toa_radiance,
    compute_toa_reflectance,
    classify_reflectance
)

def convert(gain, offset, dn_val, solar_zenith, earth_sun_distance,
            band_choice, custom_esun):
    # Determine E_sun
    if band_choice == "Custom":
        esun = custom_esun
    else:
        esun = get_esun_for_band(band_choice)
    
    if esun is None or esun <= 0:
        return ("", "", "Invalid E_sun value. Check band selection or custom entry.")
    
    # Compute radiance
    L = compute_toa_radiance(dn_val, gain, offset)
    # Compute reflectance
    rho = compute_toa_reflectance(L, earth_sun_distance, esun, solar_zenith)
    # Classification
    classification = classify_reflectance(rho)
    
    radiance_str = f"{L:.6f} W/m²/sr/µm"
    reflectance_str = f"{rho:.6f}"
    return (radiance_str, reflectance_str, classification)

def toggle_custom_esun(band):
    return gr.update(visible=(band == "Custom"))

# Build the Gradio interface
with gr.Blocks(title="TOA Reflectance Converter") as demo:
    gr.Markdown("# TOA Reflectance Converter")
    with gr.Row():
        with gr.Column():
            gain = gr.Number(label="Calibration Gain (DN per radiance unit)", value=0.0000271)
            offset = gr.Number(label="Calibration Offset", value=0.0)
            dn = gr.Number(label="Digital Number (DN) [0–65535]", value=100, precision=0)
            solar_zenith = gr.Number(label="Solar Zenith Angle θ (degrees) [0–90]", value=30.0)
            distance = gr.Number(label="Earth–Sun Distance d (AU)", value=1.0)
            band = gr.Dropdown(
                choices=get_band_names() + ["Custom"],
                value=get_band_names()[0],
                label="Satellite Band"
            )
            custom_esun = gr.Number(label="Custom E_sun (W/m²/µm)", value=None, visible=False)
            compute_btn = gr.Button("Compute")
        with gr.Column():
            out_rad = gr.Textbox(label="TOA Radiance (L)", interactive=False)
            out_ref = gr.Textbox(label="TOA Reflectance (ρ)", interactive=False)
            out_cls = gr.Textbox(label="Classification", interactive=False)
    
    band.change(fn=toggle_custom_esun, inputs=band, outputs=custom_esun)
    
    compute_btn.click(
        fn=convert,
        inputs=[gain, offset, dn, solar_zenith, distance, band, custom_esun],
        outputs=[out_rad, out_ref, out_cls]
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
