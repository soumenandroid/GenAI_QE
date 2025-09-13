from fastapi import FastAPI

app = FastAPI()

# Fake locator mapping (like GenAI “healed” output)
LOCATOR_MAP = {
    "username": "//input[@placeholder='Username or Email Address']",
    "password": "//input[@placeholder='Password']",
    "loginBtn": "//button[@type='submit']"
}

@app.get("/selfheal")
def self_heal(locatorKey: str):
    return {"healed_locator": LOCATOR_MAP.get(locatorKey, "")}
