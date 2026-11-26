"""Generate every missing recipe and chapter photo in parallel (skips images that already exist)."""
import sys, pathlib, time, concurrent.futures as cf
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import gen_image, image_prompts as P, recipes as R

OUT = gen_image.OUT
jobs = [(R.slug(t), s, "4:3") for t, s in P.PROMPTS.items()]
jobs += [(f"chapter-{n:02d}", s, "4:5") for n, s in P.CHAPTERS.items()]
todo = [j for j in jobs if not (OUT / f"{j[0]}.jpg").exists()]
print(f"{len(jobs)} images, {len(todo)} to generate", flush=True)

def work(job):
    slug, subject, aspect = job
    for attempt in range(4):
        try:
            gen_image.generate(slug, subject, aspect)
            return slug, "ok"
        except Exception as ex:  # retry with backoff
            err = ex; time.sleep(5 * (attempt + 1))
    return slug, f"FAILED: {err}"

done = 0
with cf.ThreadPoolExecutor(max_workers=6) as ex:
    for slug, status in ex.map(work, todo):
        done += 1
        print(f"[{done}/{len(todo)}] {slug}: {status}", flush=True)
