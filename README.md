# SuperAnnotate Hexagon Annotation Task

This project creates a **hexagon annotation** on an image using SuperAnnotate’s SDK and the official **Modern Image Project format**.

---

## Branch Strategy

The project uses two separate branches to isolate logic testing from API interactions:

| Branch          | Purpose                                 | SA API Calls | Image Required |
|-----------------|------------------------------------------|----------|--------------|
| `main`          | Local testing with mock data (no API)    | No       | No           |
| `sa-api-version`| Full flow using SuperAnnotate SDK        | Yes      | Yes (in `images/`) |

> This approach ensures API rate limits are respected and testing can be done offline.

---

## Contents

- `superannotate_task.py` – Main Python script
- `images/sample3.jpg` – Local image used in API flow (only in `sa-api-version`)
- `hex_annotation_test.json` – Sample annotation output
- `.env` – Stores your SA token (excluded from GitHub)
- `requirements.txt` – Reproducible dependency list

---

## Steps Performed

1. Create Image Project of type `Vector`
2. Add annotation class: `hexagon` (polygon)
3. Attach an image via URL or local path
4. Generate hexagonal points dynamically
5. Save annotations using the required `<image_name>___objects.json` naming convention
6. Upload annotation and mark the image as `Completed`

---

## Annotation Format

The annotation JSON follows SuperAnnotate’s official schema:
- `metadata`: includes name, width, height, and status
- `instances`: holds the hexagon polygon
- `tags`: optional keywords (e.g., `"generated"`)
- `comments`: empty by default

---

## Validation

The image was uploaded and validated using:

```python

sa_client.upload_annotation(...)

## Exported Annotations

This project includes SDK-exported annotations in the `/exported_annotations/` folder, containing:

- `classes.json`: class metadata
- `sample3.jpg.json`: annotation file in SuperAnnotate schema

These are programmatically downloaded via the SDK and can be used for audit or verification.