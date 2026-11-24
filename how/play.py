"""Record each built game being played with real keypresses (headless Playwright).
The bot reads object positions from the page to choose keys; it never changes game state.
Usage: venv/bin/python play.py <name> <html> <out_dir> <seconds>"""
import sys, time, json, http.server, threading, functools, pathlib
from playwright.sync_api import sync_playwright
name, html, out, secs = sys.argv[1], pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3]), float(sys.argv[4])
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(html.parent)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
# player x and obstacle list per game (top-level let/const are visible to page.evaluate)
PEEK = {"g60": "[p.x, rocks.map(r=>[r.x,r.y,r.r]), over]",
        "g30": "[p, r.map(o=>[o.x,o.y,o.w/2]), over]",
        "g10": "[p.x, r.map(b=>[b.x,b.y,8]), o]"}[name]
PY = {"g60": "p.y", "g30": "570", "g10": "p.y"}[name]
with sync_playwright() as pw:
    b = pw.chromium.launch(headless=True)
    ctx = b.new_context(viewport={"width": 540, "height": 960}, record_video_dir=str(out), record_video_size={"width": 540, "height": 960})
    pg = ctx.new_page()
    t0 = time.time()
    pg.goto(f"http://127.0.0.1:{srv.server_port}/{html.name}")
    pg.add_style_tag(content="html,body{height:960px!important}canvas{width:500px!important;height:auto!important;display:block;margin:auto}")
    log, held, deaths = [], None, []
    start = time.time()
    while time.time() - start < secs:
        px, obs, dead = pg.evaluate(PEEK)
        py = pg.evaluate(PY)
        if dead:
            deaths.append(round(time.time() - t0, 2))
            if held: pg.keyboard.up(held); held = None
            time.sleep(1.2); pg.keyboard.press("Space"); continue
        danger = [o for o in obs if py - 160 < o[1] < py + 20]
        best, want = None, None
        W = {"g60": 480, "g30": 400, "g10": 400}[name]
        for cand in (px - 40, px, px + 40):
            if not 15 <= cand <= W - 15: continue
            c = sum(1 / (abs(o[0] - cand) + 1) for o in danger if abs(o[0] - cand) < o[2] + 30) + abs(cand - W / 2) / 20000
            if best is None or c < best: best, want = c, cand
        key = None if abs(want - px) < 3 else ("ArrowLeft" if want < px else "ArrowRight")
        if key != held:
            if held: pg.keyboard.up(held)
            if key: pg.keyboard.down(key)
            held = key
        time.sleep(0.03)
    pg.close(); ctx.close(); b.close()
    vid = sorted(out.glob("*.webm"), key=lambda p: p.stat().st_mtime)[-1]
    vid.rename(out / f"{name}.webm")
    json.dump({"load_offset_s": 0, "deaths_s": deaths}, open(out / f"{name}.json", "w"))
    print(name, "deaths at", deaths)
