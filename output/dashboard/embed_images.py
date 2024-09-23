import base64
import re
from pathlib import Path

def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def convert_html_with_local_images(html_content, visualisations_path):
    def replace_image(match):
        image_path = match.group(1)
        full_path = visualisations_path / Path(image_path).name
        if full_path.exists():
            try:
                base64_image = image_to_base64(full_path)
                return f'src="data:image/png;base64,{base64_image}"'
            except FileNotFoundError:
                print(f"Warning: Image file not found: {full_path}")
                return match.group(0)
        return match.group(0)

    # Replace background-image URLs
    pattern = r'background-image:\s*url\([\'"]?([^)]+\.png)[\'"]?\)'
    html_content = re.sub(pattern, lambda m: f'background-image: url(data:image/png;base64,{image_to_base64(visualisations_path / Path(m.group(1)).name)})', html_content)

    # Replace img src URLs
    pattern = r'src=[\'"]?([^\'"]+\.png)[\'"]?'
    html_content = re.sub(pattern, replace_image, html_content)

    return html_content

# Define paths
project_root = Path(__file__).parent.parent.parent
input_html_path = project_root / "src" / "dashboard.html"
output_html_path = project_root / "output" / "dashboard" / "dashboard_embedded.html"
visualisations_path = project_root / "output" / "visualisations"

# Read the original HTML content
with open(input_html_path, "r") as file:
    original_html_content = file.read()

# Convert the HTML content with embedded images
embedded_html_content = convert_html_with_local_images(original_html_content, visualisations_path)

# Save the embedded HTML content to a new file
with open(output_html_path, "w") as file:
    file.write(embedded_html_content)

print(f"Embedded HTML file created: {output_html_path}")    