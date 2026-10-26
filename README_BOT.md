# README_BOT: adding the nightly superfan update

Site: https://kansascashsuperfan.github.io (repo kansascashsuperfan/kansascashsuperfan.github.io, branch `main`, root).
Static HTML, no build step: `add_update.py` writes `updates/YYYY-MM-DD.json` and regenerates `index.html`
from `template.html` (newest first). `.nojekyll` disables Jekyll. Edit look in `style.css` / `template.html`.

## Nightly steps
1. **X posts**: `x` MCP connector → `get_users_posts` with `id=1275447541585211394` (@Kansas_Cash),
   `max_results=40`, `post.fields=created_at,public_metrics,referenced_tweets,in_reply_to_user_id,attachments`,
   `expansions=referenced_tweets.id,in_reply_to_user_id,attachments.media_keys`, `user.fields=username`.
   Keep posts from the last ~24h (created_at is UTC; convert to America/Chicago).
   Link: `https://x.com/Kansas_Cash/status/<id>`.
2. **Stocktwits**:
   `curl -s -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130.0 Safari/537.36" https://api.stocktwits.com/api/2/streams/user/kansascash.json`
   → `messages[]` (`id`, `created_at` UTC, `body`, `likes.total`). Link: `https://stocktwits.com/KansasCash/message/<id>`.
   Note: bodies may contain HTML entities (e.g. `&#39;`); unescape them before quoting.
3. **Write the entry** (JSON, see format in `add_update.py` docstring): `date` (Chicago date), `intro`,
   and 5–8 `items` with `platform` (`x`/`stocktwits`), `caption`, optional `quote` (exact text), `when`, `likes`, `url`.
   Voice: affectionate hype-man superfan, funny, PG. Only describe what posts actually say; don't invent.
   Skip divisive political posts. If the day was quiet, cover the last couple of days and say so in `intro`.
   Never use his real name; persona display name is "Kansas Cash Superfan".
4. **Add + publish**:
   ```bash
   cd /home/box/agent-data/agents/6f7bdc7f-533f-4809-a709-92a6f6f705ae/fansite
   git pull --ff-only
   python3 add_update.py /workspace/entry-YYYY-MM-DD.json   # same date again = replace
   git add -A && git commit -m "Update for YYYY-MM-DD" && git push
   ```
   Git identity (already set in repo config): `Kansas Cash Superfan <348402677+kansascashsuperfan@users.noreply.github.com>`.
5. **Verify**: `gh api repos/kansascashsuperfan/kansascashsuperfan.github.io/pages/builds/latest --jq .status`
   until `built`, then `curl -s https://kansascashsuperfan.github.io | grep u-YYYY-MM-DD`.
