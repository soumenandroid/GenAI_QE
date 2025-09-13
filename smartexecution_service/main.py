''' ---------------- import -------------
FastAPI → defines your REST endpoints.
Pydantic → validates request payloads (HealRequest).
db.get_connection → SQLite connection for caching healed locators.
OpenAI → to call GPT for healing broken locators.
dotenv → loads OPENAI_API_KEY from .env.
re → regex for cleaning/validating selectors.
'''

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from db import get_connection
from openai import OpenAI
from dotenv import load_dotenv
import os, re

load_dotenv()

app = FastAPI()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------- Models ----------
class HealRequest(BaseModel):
    locatorKey: str
    original_locator: str
    html_snippet: str

# ---------- Cleaning & Validation ----------
CODE_FENCE_RE = re.compile(r"```(?:[a-zA-Z]+)?\s*([\s\S]*?)\s*```", re.MULTILINE)

def clean_selector(raw: str) -> str:
    """
    Turn arbitrary LLM text into a raw Selenium selector string.
    - Strips ```css/```xpath fences
    - Removes surrounding quotes
    - Unescapes JSON escapes (\\" -> ", \\n -> space)
    - Normalizes quotes for CSS (double -> single)
    """
    if not raw:
        return ""

    txt = raw.strip()

    # If wrapped in code fences, take inner content
    m = CODE_FENCE_RE.search(txt)
    if m:
        txt = m.group(1)

    # Unescape common JSON escapes
    txt = txt.replace("\\n", " ").replace("\n", " ").replace("\r", " ")
    txt = txt.replace('\\"', '"').replace("\\'", "'")

    # Trim surrounding quotes
    if (txt.startswith('"') and txt.endswith('"')) or (txt.startswith("'") and txt.endswith("'")):
        txt = txt[1:-1].strip()

    # Collapse extra spaces
    txt = re.sub(r"\s+", " ", txt).strip()

    # For CSS (not XPath), normalize " to ' to avoid escaping in JSON
    if not (txt.startswith("/") or txt.startswith("(")):  # likely CSS
        txt = txt.replace('"', "'")

    return txt

def _balanced(s: str, left: str, right: str) -> bool:
    count = 0
    for ch in s:
        if ch == left: count += 1
        elif ch == right: count -= 1
        if count < 0: return False
    return count == 0

CSS_ALLOWED = re.compile(
    r"^[a-zA-Z0-9\s\#\.\-\_\:\,\>\+\~\*\^\$\|\=\(\)\[\]\"']+$"
)

def is_valid_selector(sel: str) -> bool:
    """
    Very permissive validation that accepts real-world CSS & XPath.
    """
    if not sel:
        return False

    # XPath: starts with / or (
    if sel.startswith("/") or sel.startswith("("):
        # rudimentary sanity: contains brackets or @ or // or //* etc.
        return bool(re.search(r"//|@|\[|\]", sel))

    # Otherwise treat as CSS:
    if not CSS_ALLOWED.fullmatch(sel):
        return False

    # Structural checks for CSS
    if not _balanced(sel, "[", "]"): return False
    if not _balanced(sel, "(", ")"): return False
    # Quote counts (either both even or zero)
    if sel.count("'") % 2 != 0: return False
    if sel.count('"') % 2 != 0: return False

    return True

# ---------- Endpoints ----------
@app.post("/selfheal")
def self_heal(req: HealRequest):
    conn = get_connection()
    cur = conn.cursor()

    # 1) Cache
    cur.execute("SELECT locator FROM locator_map WHERE key = ?", (req.locatorKey,))
    row = cur.fetchone()
    if row:
        return {"healed_locator": row[0]}

    # 2) Prompt LLM
    prompt = f"""
You are a Selenium test assistant. A locator is broken.

Locator Key: {req.locatorKey}
Original Locator: {req.original_locator}

HTML snippet:
{req.html_snippet}

Task:
Return ONLY a valid Selenium CSS selector or XPath that identifies the element.
No explanations. No markdown. Only the selector string.
"""

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=80,
            temperature=0.2,
        )
        healed_raw = resp.choices[0].message.content.strip()
        healed = clean_selector(healed_raw)

        # DEBUG (optional): print what came vs stored
        # print("RAW:", healed_raw)
        # print("CLEANED:", healed)

        if not is_valid_selector(healed):
            # Do NOT cache invalid suggestions
            return {"error": f"Invalid AI suggestion: {healed_raw}"}

        # 3) Cache valid suggestion
        conn.execute(
            "INSERT OR REPLACE INTO locator_map (key, locator) VALUES (?, ?)",
            (req.locatorKey, healed),
        )
        conn.commit()
        return {"healed_locator": healed}

    except Exception as e:
        return {"error": str(e)}

@app.delete("/locator/{key}")
def delete_locator(key: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM locator_map WHERE key = ?", (key,))
    conn.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Locator not found")
    return {"message": f"Deleted locator with key: {key}"}

@app.delete("/locators")
def delete_all_locators():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM locator_map")
    conn.commit()
    return {"status": "success", "message": "All locators deleted"}

@app.get("/locators")
def list_locators():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT key, locator FROM locator_map ORDER BY key")
    rows = cur.fetchall()
    return [{"key": k, "locator": v} for (k, v) in rows]
