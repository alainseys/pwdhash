import os
import crypt
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Special characters allowed
SPECIAL_CHARS = "!@#$%^&*()_+-=[]{}|;:,.<>?"
MIN_LENGTH = 5


def validate_password(pwd: str):
    """Return (is_valid: bool, errors: list)"""
    errors = []

    if len(pwd) < MIN_LENGTH:
        errors.append(f"Minimum {MIN_LENGTH} characters required.")

    if not any(c.isupper() for c in pwd):
        errors.append("At least one uppercase letter required.")

    if not any(c.isdigit() for c in pwd):
        errors.append("At least one number required.")

    if not any(c in SPECIAL_CHARS for c in pwd):
        errors.append("At least one special character required: !@#$%^&*()_+-=[]{}|;:,.<>?")

    return (len(errors) == 0, errors)


def crypt_sha256(password: str) -> str:
    """
    Generate SHA-256 crypt hash in format: $5$salt$hash
    Uses 16-character random salt (default for METHOD_SHA256)
    """
    salt = crypt.mksalt(crypt.METHOD_SHA256)  # e.g. $5$rounds=535000$somesalt$
    return crypt.crypt(password, salt)


@app.route("/", methods=["GET", "POST"])
def index():
    # Fresh visit → clear session
    if request.method == "GET":
        session.pop("hash_shown", None)
        return render_template("index.html")

    if request.method == "POST":
        action = request.form.get("action")
        password = request.form.get("password", "").strip()

        # Prevent re-submission after hash shown
        if session.get("hash_shown"):
            return redirect(url_for("index"))

        if action == "check" and password:
            is_valid, errors = validate_password(password)

            if not is_valid:
                return render_template("index.html", errors=errors)

            # Valid → generate crypt SHA-256 hash ONCE
            h = crypt_sha256(password)
            session["hash_shown"] = True
            return render_template("index.html", hash_value=h, hash_type="SHA-256 (crypt)")

    return redirect(url_for("index"))


# === START SERVER ===
if __name__ == '__main__':
    print("\n=== FLASK URL MAP ===")
    for rule in app.url_map.iter_rules():
        methods = ','.join(sorted(rule.methods))
        print(f"{methods:12} {rule}")
    print("======================\n")
    from waitress import serve
    serve(app, host="0.0.0.0", port=8085)
