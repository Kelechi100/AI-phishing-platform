import re

def calculate_risk_score(sender: str, subject: str, body: str):

    score = 0
    reasons = []

    content = f"{subject} {body}".lower()

    #  Urgency keywords
    urgency_words = ["urgent", "immediately", "asap", "suspended", "verify", "action required"]

    for word in urgency_words:
        if word in content:
            score += 10
            reasons.append(f"Urgency keyword detected: {word}")

    #  Suspicious domains
    suspicious_domains = ["secure-login", "update-account", "verify-now", "banking-alert"]

    if any(domain in sender for domain in suspicious_domains):
        score += 20
        reasons.append("Suspicious sender domain")

    # Fake payment links
    url_pattern = r"http[s]?://[^\s]+"

    urls = re.findall(url_pattern, body)

    for url in urls:
        if any(keyword in url for keyword in ["paypal", "bank", "secure", "login"]):
            score += 15
            reasons.append(f"Suspicious payment-related URL detected: {url}")

    # Random digits in sender
    if sum(char.isdigit() for char in sender) > 3:
        score += 10
        reasons.append("Too many digits in sender address")

    # Cap score
    score = min(score, 100)

    return score, reasons