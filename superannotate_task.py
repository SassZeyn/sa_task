import os
import json
import math
from dotenv import load_dotenv
from PIL import Image  # New: to read actual image size

# === Step 1: Image file setup ===
image_name = "sample3.jpg"
image_path = os.path.join("images", image_name)

# === Step 2: Read image dimensions ===
with Image.open(image_path) as img:
    width, height = img.size

# === Step 3: Hexagon point generator ===
def generate_hexagon_points(width, height, scale=0.4):
    cx, cy = width / 2, height / 2
    r = min(width, height) * scale / 2
    return [
        {"x": cx + r * math.cos(math.radians(angle)),
         "y": cy + r * math.sin(math.radians(angle))}
        for angle in range(0, 360, 60)
    ]

points = generate_hexagon_points(width, height)

# === Step 4: Build annotation JSON ===
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

# === Step 5: Save the JSON to local file ===
json_path = f"{image_name}___objects.json"
with open(json_path, "w") as f:
    json.dump(annotation_json, f, indent=4)

print("Local test completed. JSON file generated.")
