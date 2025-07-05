import os
import json
import math
from dotenv import load_dotenv
from superannotate import SAClient

# === Step 1: Load token and initialize SA client ===
load_dotenv()
token = os.getenv("SA_TOKEN")
sa_client = SAClient(token=token)

# === Step 2: Create Image Project ===
project_name = "HexagonAnnotationProject"
sa_client.create_project(
    name=project_name,
    project_type="Vector",
    description="Auto-generated hexagon annotation with correct naming format."
)

# === Step 3: Add Annotation Class ===
annotation_class = {
    "name": "hexagon",
    "color": "#%06x" % (int.from_bytes(os.urandom(3), "big")),
    "type": "polygon"
}
sa_client.create_annotation_class(project_name, annotation_class)

# === Step 4: Upload Image from local 'images/' folder ===
image_name = "sample3.jpg"
image_path = os.path.join("images", image_name)
sa_client.upload_images_from_folder_to_project(
    project=project_name,
    folder_path="images"
)

# === Step 5: Get Image Dimensions ===
metadata = sa_client.get_image_metadata(project_name, image_name)
width, height = metadata["width"], metadata["height"]

# === Step 6: Generate Hexagon Points ===
def generate_hexagon_points(width, height, scale=0.4):
    cx, cy = width / 2, height / 2
    r = min(width, height) * scale / 2
    return [
        {"x": cx + r * math.cos(math.radians(angle)),
         "y": cy + r * math.sin(math.radians(angle))}
        for angle in range(0, 360, 60)
    ]

points = generate_hexagon_points(width, height)

# === Step 7: Build Annotation JSON ===
annotation_json = [{
    "metadata": {
        "name": image_name,
        "width": width,
        "height": height,
        "status": "InProgress"
    },
    "instances": [{
        "type": "polygon",
        "className": "hexagon",
        "points": points
    }],
    "tags": ["generated", "hexagon"],
    "comments": []
}]

# === Step 8: Save JSON with Required Format ===
json_path = f"{image_name}___objects.json"
with open(json_path, "w") as f:
    json.dump(annotation_json, f, indent=4)

# === Step 9: Upload Annotation ===
sa_client.upload_annotation(project_name, image_name, json_path)

# === Step 10: Set Status to Completed ===
sa_client.set_image_status(project_name, image_name, "Completed")

print("Done. Annotation uploaded and marked as Completed.")
