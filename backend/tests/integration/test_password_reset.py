import getpass

from fastapi.testclient import TestClient

from app.main import app


AUTH = "/api/v1/auth"


def test_password_reset_flow():
    """Interactive end-to-end test for the password-reset flow."""

    print("\n=== NexAbility password reset integration test ===")
    email = input("Registered account email: ").strip().lower()
    old_password = getpass.getpass("Current password: ")
    new_password = getpass.getpass("New password (minimum 8 characters): ")

    assert email, "Email is required"
    assert len(new_password) >= 8, "New password must contain at least 8 characters"
    assert new_password != old_password, "Choose a password different from the current password"

    with TestClient(app) as client:
        # Login first so we can verify that password reset revokes old refresh tokens.
        print("\n[1/6] Logging in with current password...")
        old_login = client.post(
            f"{AUTH}/login",
            json={"email": email, "password": old_password},
        )
        assert old_login.status_code == 200, (
            f"Initial login failed: {old_login.status_code} {old_login.text}"
        )
        old_refresh_token = old_login.json()["refresh_token"]
        print("Initial login successful.")

        print("\n[2/6] Requesting password-reset OTP...")
        forgot_response = client.post(
            f"{AUTH}/password/forgot",
            json={"email": email},
        )
        assert forgot_response.status_code == 200, (
            f"Forgot-password request failed: "
            f"{forgot_response.status_code} {forgot_response.text}"
        )
        print(forgot_response.json())

        otp = input("Enter the password-reset OTP from your email: ").strip()
        assert otp, "OTP cannot be empty"

        print("\n[3/6] Verifying OTP...")
        verify_response = client.post(
            f"{AUTH}/otp/verify",
            json={
                "email": email,
                "purpose": "PASSWORD_RESET",
                "otp": otp,
            },
        )
        assert verify_response.status_code == 200, (
            f"OTP verification failed: "
            f"{verify_response.status_code} {verify_response.text}"
        )
        ticket = verify_response.json()["verification_ticket"]
        assert ticket, "Verification ticket was not returned"
        print("OTP verified; reset ticket received.")

        print("\n[4/6] Resetting password...")
        reset_response = client.post(
            f"{AUTH}/password/reset",
            json={
                "email": email,
                "verification_ticket": ticket,
                "new_password": new_password,
            },
        )
        assert reset_response.status_code == 200, (
            f"Password reset failed: "
            f"{reset_response.status_code} {reset_response.text}"
        )
        print(reset_response.json())

        print("\n[5/6] Checking old and new passwords...")
        old_password_response = client.post(
            f"{AUTH}/login",
            json={"email": email, "password": old_password},
        )
        assert old_password_response.status_code == 401, (
            "Old password should no longer work. "
            f"Received {old_password_response.status_code}: "
            f"{old_password_response.text}"
        )

        new_password_response = client.post(
            f"{AUTH}/login",
            json={"email": email, "password": new_password},
        )
        assert new_password_response.status_code == 200, (
            f"New password login failed: "
            f"{new_password_response.status_code} {new_password_response.text}"
        )
        print("Old password rejected; new password accepted.")

        print("\n[6/6] Checking ticket reuse and refresh-token revocation...")
        reused_ticket_response = client.post(
            f"{AUTH}/password/reset",
            json={
                "email": email,
                "verification_ticket": ticket,
                "new_password": old_password,
            },
        )
        assert reused_ticket_response.status_code == 400, (
            "A consumed reset ticket should not be reusable. "
            f"Received {reused_ticket_response.status_code}: "
            f"{reused_ticket_response.text}"
        )

        old_refresh_response = client.post(
            f"{AUTH}/refresh",
            json={"refresh_token": old_refresh_token},
        )
        assert old_refresh_response.status_code == 401, (
            "The refresh token issued before password reset should be revoked. "
            f"Received {old_refresh_response.status_code}: "
            f"{old_refresh_response.text}"
        )

        print("\nSUCCESS: password reset, old-password rejection, new-password login,")
        print("one-time ticket consumption, and refresh-token revocation all passed.")
