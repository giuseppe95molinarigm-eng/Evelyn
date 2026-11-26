"""Generate a recipe photo with FLUX dev on Replicate, then upscale x2 with Real-ESRGAN.

Usage: REPLICATE_API_TOKEN=... python3 tools/gen_image.py <slug> "<subject description>" [--seed N]
The token is read from the environment only and never written to disk.
"""
import json, os, sys, time, urllib.request, pathlib

TOKEN = os.environ["REPLICATE_API_TOKEN"]
API = "https://api.replicate.com/v1"
OUT = pathlib.Path(__file__).resolve().parent.parent / "layout" / "images"

# Shared house style so all 150 photos look like one book: bright, airy, light wood, cream linen, sage accents.
STYLE = ("professional editorial food photography for a cookbook, bright airy farmhouse kitchen, "
         "light natural oak wood table, cream linen napkin, subtle sage green accents, soft natural window light from the left, "
         "warm and inviting, shallow depth of field, 45-degree angle, high detail, appetizing, "
         "no text, no labels, no writing, no people")

def call(url, payload=None, method="POST"):
    req = urllib.request.Request(url, method=method, data=json.dumps(payload).encode() if payload else None,
                                 headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json", "Prefer": "wait",
                                          "User-Agent": "cookbook-image-tool/1.0"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.load(r)

def run(url, payload):
    p = call(url, payload)
    while p["status"] not in ("succeeded", "failed", "canceled"):
        time.sleep(2)
        p = call(p["urls"]["get"], method="GET")
    if p["status"] != "succeeded":
        raise SystemExit(f"prediction {p['status']}: {p.get('error')}")
    return p["output"]

def generate(slug, subject, aspect="4:3", seed=None):
    inp = {"prompt": f"{subject}. {STYLE}", "aspect_ratio": aspect, "output_format": "png",
           "num_inference_steps": 28, "guidance": 3, "go_fast": False}
    if seed is not None: inp["seed"] = seed
    out = run(f"{API}/models/black-forest-labs/flux-dev/predictions", {"input": inp})
    src = out[0] if isinstance(out, list) else out
    ver = call(f"{API}/models/nightmareai/real-esrgan", method="GET")["latest_version"]["id"]
    up = run(f"{API}/predictions", {"version": ver, "input": {"image": src, "scale": 2, "face_enhance": False}})
    OUT.mkdir(parents=True, exist_ok=True)
    png = OUT / f"{slug}.png"
    req = urllib.request.Request(up if isinstance(up, str) else up[0], headers={"User-Agent": "cookbook-image-tool/1.0"})
    png.write_bytes(urllib.request.urlopen(req, timeout=180).read())
    # Save as high-quality JPEG for the layout
    from PIL import Image
    jpg = OUT / f"{slug}.jpg"
    Image.open(png).convert("RGB").save(jpg, quality=92, dpi=(300, 300))
    png.unlink()
    return jpg

if __name__ == "__main__":
    seed = int(sys.argv[sys.argv.index("--seed") + 1]) if "--seed" in sys.argv else None
    print(generate(sys.argv[1], sys.argv[2], seed=seed))
