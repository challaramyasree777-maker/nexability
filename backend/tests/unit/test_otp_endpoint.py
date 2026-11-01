"""
Manual end-to-end test for NexAbility OTP endpoints.

Run from the backend directory:
    python test_otp_endpoints.py

The script requests an OTP, waits for you to enter the code received in your
inbox, and then calls the OTP verification endpoint.
"""
import json
import urllib.error
import urllib.request

BASE_URL = "http://127.0.0.1:8000/api/v1/auth"


def post_json(path: str, payload: dict) -> tuple[int, dict]:
    request = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read().decode("utf-8")
            return response.status, json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8")
        try:
            return exc.code, json.loads(body)
        except json.JSONDecodeError:
            return exc.code, {"detail": body}
    except urllib.error.URLError as exc:
        raise RuntimeError(
            f"Cannot connect to {BASE_URL}. Is Uvicorn running? {exc}"
        ) from exc


def main() -> None:
    print("\nNexAbility OTP endpoint test")
    print("----------------------------")
    print("1. Candidate registration")
    print("2. Employer registration")
    choice = input("Choose flow (1 or 2): ").strip()

    purposes = {
        "1": "CANDIDATE_REGISTRATION",
        "2": "EMPLOYER_REGISTRATION",
    }
    purpose = purposes.get(choice)
    if purpose is None:
        print("Invalid choice.")
        return

    email = input("Enter an email address you can access: ").strip()
    if not email:
        print("Email is required.")
        return

    print("\nRequesting OTP...")
    status, result = post_json(
        "/otp/send",
        {"email": email, "purpose": purpose},
    )
    print(f"HTTP {status}: {json.dumps(result, indent=2)}")

    if not 200 <= status < 300:
        print("OTP request failed. Check the response above.")
        return

    otp = input("\nEnter the OTP received in your inbox: ").strip()
    if not otp:
        print("OTP is required.")
        return

    print("\nVerifying OTP...")
    status, result = post_json(
        "/otp/verify",
        {"email": email, "purpose": purpose, "otp": otp},
    )
    print(f"HTTP {status}: {json.dumps(result, indent=2)}")

    if 200 <= status < 300 and result.get("verified") is True:
        print("\nSUCCESS: OTP was sent and verified.")
    else:
        print("\nFAILED: OTP verification did not succeed.")


if __name__ == "__main__":
    main()
