import os
import json
import math
import random
import uuid
from datetime import datetime
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import requests
from superannotate import SAClient

# === Step 0: Load API token from environment ===
load_dotenv()
token = os.getenv("SA_TOKEN")
if not token:
    raise ValueError("SA_TOKEN not found in .env file")

# === Step 1: Initialize SAClient ===
sa = SAClient(token=token)

# === Step 2: Create a new Image Project ===
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
project_name = f"HexagonProject_{timestamp}"
sa.create_project(
    project_name=project_name,
    project_description="Project with hexagon annotation",
    project_type="Vector"
)
print(f"[✓] Project created: {project_name}")

# === Step 3: Create an Annotation Class with random color ===
class_name = "Hexagon"
hex_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
sa.create_annotation_class(
    project=project_name,
    name=class_name,
    color=hex_color,
    class_type="object"
)
print(f"[✓] Annotation class '{class_name}' created with color {hex_color}")

# === Step 4: Attach image from GitHub raw URL ===
image_name = "sample3.jpg"
image_url = "https://raw.githubusercontent.com/SassZeyn/sa_task/sa-api-version/images/sample3.jpg"
sa.attach_items(
    project=project_name,
    attachments=[{"name": image_name, "url": image_url}],
    annotation_status="NotStarted"
)
print(f"[✓] Image attached: {image_name}")

# === Step 5: Get image dimensions from the image itself ===
response = requests.get(image_url)
if not response.ok:
    raise Exception(f"Failed to download image from URL: {image_url}")
image = Image.open(BytesIO(response.content))
width, height = image.size
print(f"[✓] Fetched image dimensions: width={width}, height={height}")

# === Step 6: Generate hexagon polygon points (flattened) ===
def generate_hexagon_points(width, height, scale=0.4):
    cx, cy = width / 2, height / 2
    r = min(width, height) * scale / 2
    return [[cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))] for a in range(0, 360, 60)]

hexagon_points = generate_hexagon_points(width, height)
flat_points = [coord for point in hexagon_points for coord in point]  # Flattened list

# === Step 7: Get classId ===
classes = sa.search_annotation_classes(project=project_name, name_contains=class_name)
if not classes:
    raise ValueError("Annotation class not found.")
class_id = classes[0]['id']

# === Step 8: Prepare annotation JSON ===
annotation = {
    "metadata": {
        "name": image_name,
        "width": width,
        "height": height
    },
    "instances": [
        {
            "id": str(uuid.uuid4()),
            "type": "polygon",
            "classId": class_id,
            "className": class_name,
            "probability": 100,
            "points": flat_points,
            "groupId": 0,
            "pointLabels": {},
            "attributes": [],
            "locked": False
        }
    ],
    "tags": [],
    "comments": []
}

# === Step 9: Upload annotation ===
sa.upload_annotations(project=project_name, annotations=[annotation])
print(f"[✓] Annotation uploaded for image: {image_name}")

# === Step 10: Set image status to 'Completed' ===
sa.set_annotation_statuses(
    project=project_name,
    annotation_status="Completed",
    items=[image_name]
)
print(f"[✓] Image status set to Completed: {image_name}")

# === Step 11: Save annotation JSON locally ===
json_filename = f"{image_name.rsplit('.', 1)[0]}.json"
with open(json_filename, "w") as f:
    json.dump(annotation, f, indent=2)
print(f"[✓] Annotation JSON saved as: {json_filename}")

# === Step 12: Download annotation via SDK for verification ===
export_path = "./exported_annotations"
os.makedirs(export_path, exist_ok=True)

sa.download_annotations(
    project=project_name,
    path=export_path,
    items=[image_name]
)
print(f"[✓] Annotation downloaded via SDK to: {os.path.join(export_path, image_name + '.json')}")
