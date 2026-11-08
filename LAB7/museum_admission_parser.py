import datetime
import re

MIN_AGE = 0
MAX_AGE = 120
_DATE_PATTERN = re.compile(r"(\d{4})-(\d{2})-(\d{2})", re.ASCII)


def format_visitor_name(name):
    """
    Formats a full name as 'Surname, Given names' for the ticket.
    Returns None if name is not a string or contains no words.

    Bugs fixed (found by fuzzing):
      - None / non-string input  -> AttributeError on .split()
      - '' or whitespace only    -> IndexError on parts[-1]
      - single word ('asha')     -> produced 'Asha, ' with a dangling comma
    """
    if not isinstance(name, str):
        return None
    parts = name.split()
    if not parts:
        return None
    surname = parts[-1].title()
    if len(parts) == 1:
        return surname
    return surname + ', ' + ' '.join(parts[:-1]).title()


def parse_group_ages(text):
    """
    Parses space-separated ages into a list of ints.
    Returns None if text is not a string, is empty, or contains any value
    that is not a whole number between MIN_AGE and MAX_AGE.

    Bugs fixed (found by fuzzing):
      - None / non-string input           -> AttributeError on .split()
      - non-numeric tokens ('abc', '1.5') -> ValueError from int()
      - Unicode digits like '²'           -> isdigit() is True but int() fails
      - '1_0', '+5', '-3', '999'          -> silently accepted as ages
    """
    if not isinstance(text, str):
        return None
    tokens = text.split()
    if not tokens:
        return None
    ages = []
    for token in tokens:
        # Only plain ASCII digits: rejects signs, underscores, decimals, Unicode digits
        if not (token.isascii() and token.isdigit()):
            return None
        age = int(token)
        if not (MIN_AGE <= age <= MAX_AGE):
            return None
        ages.append(age)
    return ages


def parse_visit_date(text):
    """
    Parses a YYYY-MM-DD date into a (year, month, day) tuple.
    Returns None if text is not a string or is not a real calendar date.

    Bugs fixed (found by fuzzing):
      - None / non-string input          -> AttributeError on .strip()
      - wrong number of dashes ('', '1-2', '1-2-3-4') -> ValueError on unpack
      - non-numeric parts ('a-b-c')      -> ValueError from int()
      - impossible dates ('2026-13-45', '2026-02-30') were accepted
    """
    if not isinstance(text, str):
        return None
    match = _DATE_PATTERN.fullmatch(text.strip())
    if match is None:
        return None
    year, month, day = (int(part) for part in match.groups())
    try:
        datetime.date(year, month, day)
    except ValueError:
        return None
    return year, month, day


def main():
    print("==== Running format_visitor_name ====")
    value = input("Enter a visitor's full name (e.g. asha rao): ")
    result = format_visitor_name(value)
    if result is None:
        print("Invalid name: please enter at least one word.")
    else:
        print("Name on ticket:", result)

    print("\n==== Running parse_group_ages ====")
    value = input("Enter the ages in the group separated by spaces (e.g. 34 12 70): ")
    result = parse_group_ages(value)
    if result is None:
        print(f"Invalid ages: enter whole numbers between {MIN_AGE} and {MAX_AGE} separated by spaces.")
    else:
        print("Group ages:", result)

    print("\n==== Running parse_visit_date ====")
    value = input("Enter the visit date as YYYY-MM-DD (e.g. 2026-11-05): ")
    result = parse_visit_date(value)
    if result is None:
        print("Invalid date: enter a real date in YYYY-MM-DD format.")
    else:
        print("Visit date (year, month, day):", result)


if __name__ == "__main__":
    main()
