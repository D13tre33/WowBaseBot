import re


class Regex:
    deep_link = re.compile(r"^start [0-9a-zA-Z-_]{1,32}$")
    email = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b")
    phone_number = \
        re.compile(r"\+?7 ?(\d{3}[-.\s]??\d{3}[-.\s]??\d{4}|"
                   r"\(\d{3}\)\s*\d{3}[-.\s]??\d{4}|\d{3}[-.\s]??\d{4}|"
                   r"\d{3}[-.\s]??\d{3}[-.\s]??\d{2}[-.\s]??\d{2}[-.\s]|"
                   r"\(\d{3}\)\s*\d{3}[-.\s]??\d{2}[-.\s]??\d{2}[-.\s]|"
                   r"\d{3}[-.\s]??\d{2}[-.\s]??\d{2}[-.\s])")
    username = re.compile(r"^@?[a-zA-Z0-9_]{5,32}$")
    int = re.compile(r"^-?[0-9]+$")
    username_or_id = re.compile(r"(^@?[a-zA-Z0-9_]{5,32}$|^-?[0-9]+$)")
    count = re.compile(r"^[0-9]+$")
    user_id = re.compile(r"[0-9]{1,32}$")
    uuid4 = re.compile(r"^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z", re.I)
