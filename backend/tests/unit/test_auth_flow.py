"""
NexAbility end-to-end candidate authentication test.

Run from the backend directory:
    pytest -v -s tests/integration/test_auth_e2e.py

This test starts from a new candidate registration and continues through:
1. Send registration OTP to the configured email.
2. Verify the OTP and receive a verification ticket.
3. Register the candidate using that ticket.
4. Log in with the newly created credentials.
5. Access the protected /me endpoint.
6. Refresh tokens and verify rotation.
7. Reject reuse of the old refresh token.
8. Log out and verify the current refresh token is revoked.

The test uses the real configured database and email provider. It creates
a real user and refresh-token records. It does not delete user data.

IMPORTANT:
- The email below is the address requested for this test.
- You must be able to receive email at that address.
- If this email is already registered, registration will return HTTP 409.
- This test assumes GET /api/v1/auth/me is implemented.
"""

import getpass

from fastapi.testclient import TestClient

from app.main import app


AUTH = "/api/v1/auth"
TEST_EMAIL = "shettysuprith04@gmail.com"


def test_candidate_registration_to_logout_e2e():
    with TestClient(app) as client:
        print(f"\n=== NexAbility E2E authentication test: {TEST_EMAIL} ===")

        full_name = input("Candidate full name: ").strip()
        password = getpass.getpass("Create password (minimum 8 characters): ")

        assert len(full_name) >= 2, "Full name must contain at least 2 characters"
        assert len(password) >= 8, "Password must contain at least 8 characters"

        # STEP 1: Send registration OTP.
        print("\n[1/7] Sending registration OTP...")
        send_response = client.post(
            f"{AUTH}/otp/send",
            json={
                "email": TEST_EMAIL,
                "purpose": "CANDIDATE_REGISTRATION",
            },
        )
        assert send_response.status_code == 200, (
            f"OTP sending failed: {send_response.status_code} {send_response.text}"
        )
        print(send_response.json())

        # STEP 2: Verify OTP and receive verification ticket.
        otp = input("Enter the OTP received at the email address above: ").strip()
        assert otp, "OTP cannot be empty"

        print("\n[2/7] Verifying OTP...")
        verify_response = client.post(
            f"{AUTH}/otp/verify",
            json={
                "email": TEST_EMAIL,
                "purpose": "CANDIDATE_REGISTRATION",
                "otp": otp,
            },
        )
        assert verify_response.status_code == 200, (
            f"OTP verification failed: {verify_response.status_code} "
            f"{verify_response.text}"
        )

        verification_ticket = verify_response.json().get("verification_ticket")
        assert verification_ticket, "OTP verification did not return a verification ticket"
        print("OTP verified; verification ticket received.")

        # STEP 3: Register candidate.
        print("\n[3/7] Registering candidate...")
        register_response = client.post(
            f"{AUTH}/candidate/register",
            json={
                "full_name": full_name,
                "email": TEST_EMAIL,
                "password": password,
                "phone": None,
                "verification_ticket": verification_ticket,
            },
        )
        assert register_response.status_code == 201, (
            "Candidate registration failed. If the email is already registered, "
            "use that account's login flow instead. "
            f"HTTP {register_response.status_code}: {register_response.text}"
        )

        registered_user = register_response.json()
        assert registered_user["email"].lower() == TEST_EMAIL
        assert registered_user["role"] == "CANDIDATE"
        print("Candidate registered:", registered_user)

        # STEP 4: Login with the newly created account.
        print("\n[4/7] Logging in...")
        login_response = client.post(
            f"{AUTH}/login",
            json={
                "email": TEST_EMAIL,
                "password": password,
            },
        )
        assert login_response.status_code == 200, (
            f"Login failed: {login_response.status_code} {login_response.text}"
        )

        login_data = login_response.json()
        access_token_1 = login_data["access_token"]
        refresh_token_1 = login_data["refresh_token"]
        assert login_data["token_type"] == "bearer"
        assert access_token_1 and refresh_token_1
        print("Login successful; access and refresh tokens received.")

        # STEP 5: Access protected /me endpoint.
        print("\n[5/7] Testing protected account endpoint...")
        me_response = client.get(
            f"{AUTH}/me",
            headers={"Authorization": f"Bearer {access_token_1}"},
        )
        assert me_response.status_code == 200, (
            f"/me failed: {me_response.status_code} {me_response.text}. "
            "Confirm GET /api/v1/auth/me is implemented."
        )
        assert me_response.json()["email"].lower() == TEST_EMAIL
        assert me_response.json()["role"] == "CANDIDATE"
        print("Protected endpoint successful:", me_response.json())

        # STEP 6: Refresh tokens and verify rotation.
        print("\n[6/7] Testing refresh-token rotation...")
        refresh_response = client.post(
            f"{AUTH}/refresh",
            json={"refresh_token": refresh_token_1},
        )
        assert refresh_response.status_code == 200, (
            f"Token refresh failed: {refresh_response.status_code} "
            f"{refresh_response.text}"
        )

        refreshed_data = refresh_response.json()
        access_token_2 = refreshed_data["access_token"]
        refresh_token_2 = refreshed_data["refresh_token"]

        assert access_token_2 and refresh_token_2
        assert refresh_token_2 != refresh_token_1

        # Old refresh token must not be reusable.
        old_refresh_response = client.post(
            f"{AUTH}/refresh",
            json={"refresh_token": refresh_token_1},
        )
        assert old_refresh_response.status_code == 401, (
            "The old refresh token should be rejected after rotation: "
            f"{old_refresh_response.status_code} {old_refresh_response.text}"
        )

        # New access token must work.
        me_after_refresh = client.get(
            f"{AUTH}/me",
            headers={"Authorization": f"Bearer {access_token_2}"},
        )
        assert me_after_refresh.status_code == 200, me_after_refresh.text
        print("Refresh successful; old refresh token rejected.")

        # STEP 7: Logout and verify refresh-token revocation.
        print("\n[7/7] Logging out...")
        logout_response = client.post(
            f"{AUTH}/logout",
            json={"refresh_token": refresh_token_2},
        )
        assert logout_response.status_code == 200, (
            f"Logout failed: {logout_response.status_code} {logout_response.text}"
        )

        after_logout_response = client.post(
            f"{AUTH}/refresh",
            json={"refresh_token": refresh_token_2},
        )
        assert after_logout_response.status_code == 401, (
            "Refresh token should be rejected after logout: "
            f"{after_logout_response.status_code} {after_logout_response.text}"
        )

        print("\nSUCCESS: registration → OTP → login → /me → refresh → logout passed.")
        print(
            "Note: logout revokes refresh tokens. Existing access tokens remain "
            "valid until their short expiry unless access-token revocation is added."
        )
