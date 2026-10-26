#!/usr/bin/env python3
"""Add (or replace) one day's superfan update and regenerate index.html.

Usage:
  python3 add_update.py path/to/entry.json      # add/replace that day's update, rebuild
  python3 add_update.py --rebuild               # just rebuild index.html from updates/*.json

entry.json format:
{
  "date": "2026-10-26",                      # America/Chicago date of the update
  "intro": "Superfan caption for the day",
  "items": [
    {"platform": "x" | "stocktwits",
     "caption": "hype-man caption line",
     "quote": "exact post text (optional)",
     "when": "Mon Oct 26, 9:43 AM CT (optional)",
     "likes": 5,                              # optional
     "url": "https://x.com/Kansas_Cash/status/<id>"}
  ]
}
"""
import html, json, os, sys, datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
UPD = os.path.join(ROOT, "updates")


def esc(s):
    return html.escape(str(s), quote=True)


def render_update(u):
    d = datetime.date.fromisoformat(u["date"])
    heading = d.strftime("%A, %B ") + str(d.day) + d.strftime(", %Y")
    out = [f'<section class="update panel" id="u-{esc(u["date"])}">',
           f'  <h2>📅 {esc(heading)} <span class="meta">(Central Time)</span></h2>',
           f'  <p class="intro">{esc(u.get("intro", ""))}</p>', '  <ul>']
    for it in u["items"]:
        p = it.get("platform", "x").lower()
        badge = '<span class="badge x">𝕏</span>' if p == "x" else '<span class="badge st">Stocktwits</span>'
        meta = []
        if it.get("when"):
            meta.append(esc(it["when"]))
        if it.get("likes") not in (None, ""):
            meta.append(f'❤️ {esc(it["likes"])}')
        q = f'<span class="quote">“{esc(it["quote"])}”</span>' if it.get("quote") else ""
        m = f' <span class="meta">{" · ".join(meta)}</span>' if meta else ""
        out.append(f'    <li>{badge}{esc(it["caption"])}{q}<a href="{esc(it["url"])}">View post →</a>{m}</li>')
    out += ['  </ul>', '</section>']
    return "\n".join(out)


def rebuild():
    updates = []
    for f in sorted(os.listdir(UPD)):
        if f.endswith(".json"):
            with open(os.path.join(UPD, f)) as fh:
                updates.append(json.load(fh))
    updates.sort(key=lambda u: u["date"], reverse=True)  # newest first
    body = "\n\n".join(render_update(u) for u in updates) or '<p class="panel">No updates yet. Stay tuned, fam!</p>'
    with open(os.path.join(ROOT, "template.html")) as fh:
        tpl = fh.read()
    with open(os.path.join(ROOT, "index.html"), "w") as fh:
        fh.write(tpl.replace("<!--UPDATES-->", body))
    print(f"index.html rebuilt with {len(updates)} update(s)")


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__); sys.exit(1)
    if args[0] != "--rebuild":
        with open(args[0]) as fh:
            entry = json.load(fh)
        datetime.date.fromisoformat(entry["date"])
        assert entry.get("items"), "entry needs at least one item"
        for it in entry["items"]:
            assert it.get("url", "").startswith("https://"), f"bad url in {it}"
            assert it.get("caption"), f"missing caption in {it}"
        os.makedirs(UPD, exist_ok=True)
        with open(os.path.join(UPD, entry["date"] + ".json"), "w") as fh:
            json.dump(entry, fh, indent=2, ensure_ascii=False); fh.write("\n")
        print("saved updates/" + entry["date"] + ".json")
    rebuild()


if __name__ == "__main__":
    main()
