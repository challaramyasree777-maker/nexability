
import pytest

from app.services.email.employer_email_service import check_employer_email


@pytest.mark.parametrize(
    "email",
    [
        "test@gmail.com",
        "test@mailinator.com",
        "recruiter@microsoft.com",
        "test@nonexistentdomain.invalid",
    ],
)
def test_employer_email_screening(email):
    result = check_employer_email(email)

    assert isinstance(result, dict)
    assert "eligible" in result
    assert "reason" in result
