import dns.resolver

from free_email_domains import whitelist as free_domains
from disposable_email import is_disposable


def check_employer_email(email: str) -> dict:
    email = email.strip().lower()

    if "@" not in email:
        return {
            "eligible": False,
            "reason": "Invalid email format",
        }

    domain = email.rsplit("@", 1)[1]

    # Check 1: Free email provider
    if domain in free_domains:
        return {
            "eligible": False,
            "reason": "Please use your company email address",
        }

    # Check 2: Disposable email provider
    if is_disposable(domain):
        return {
            "eligible": False,
            "reason": "Disposable email addresses are not allowed",
        }

    # Check 3: DNS / MX records
    try:
        dns.resolver.resolve(domain, "MX")

    except dns.resolver.NXDOMAIN:
        return {
            "eligible": False,
            "reason": "Email domain does not exist",
        }

    except dns.resolver.NoAnswer:
        return {
            "eligible": False,
            "reason": "Email domain has no MX records",
        }

    except dns.resolver.NoNameservers:
        return {
            "eligible": False,
            "reason": "Unable to verify email domain",
        }

    except dns.exception.Timeout:
        return {
            "eligible": False,
            "reason": "DNS verification timed out. Please try again",
        }

    return {
        "eligible": True,
        "reason": "Company email passed initial screening",
        "domain": domain,
    }