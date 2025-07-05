import os
import json
import math
from dotenv import load_dotenv
# from superannotate import SAClient  # Commented out for local testing

# === Step 1: Skip SA token for now ===
# load_dotenv()
# token = os.getenv("SA_TOKEN")
# sa_client = SAClient(token=token)

# === Step 2: Dummy data for testing ===
image_name = "sample3.jpg"
width, height = 800, 533  # manually set for now

# === Step 3: Hexagon generator ===
def generate_hexagon_points(width, height, scale=0.4):
    cx, cy = width / 2, height / 2
    r = min(width, height) * scale / 2
    return [
        {"x": cx + r * math.cos(math.radians(angle)),
         "y": cy + r * math.sin(math.radians(angle))}
        for angle in range(0, 360, 60)
    ]

points = generate_hexagon_points(width, height)

# === Step 4: JSON Object ===
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


# === Step 5: Save locally ===
json_path = f"{image_name}___objects.json"
with open(f"{image_name}___objects.json", "w") as f:
    json.dump(annotation_json, f, indent=4)

print("✅ Local test completed. JSON file generated.")
