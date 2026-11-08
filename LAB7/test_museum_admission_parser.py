from hypothesis import given, settings, strategies as st
from museum_admission_parser import format_visitor_name, parse_group_ages, parse_visit_date

# Fuzz inputs: random Unicode text, None, and a few "near-valid" shapes so
# Hypothesis also explores inputs that look almost like real data.
name_inputs = st.text() | st.none() | st.from_regex(r"\s*[a-z]+(\s+[a-z]+)*\s*", fullmatch=True)
ages_inputs = st.text() | st.none() | st.lists(st.integers(), max_size=6).map(lambda xs: " ".join(map(str, xs)))
date_inputs = (
    st.text()
    | st.none()
    | st.from_regex(r"-?\d{1,5}(-\d{0,3}){0,3}", fullmatch=True)
    | st.dates().map(lambda d: d.isoformat())
)


@settings(max_examples=300)
@given(name_inputs)
def test_format_visitor_name_no_crash(s):
    try:
        result = format_visitor_name(s)
    except Exception as e:
        assert False, f"format_visitor_name crashed on {s!r} with: {type(e).__name__}: {e}"
    # Property: result is either None (rejected) or a non-empty string
    assert result is None or (isinstance(result, str) and result.strip() != "")


@settings(max_examples=300)
@given(ages_inputs)
def test_parse_group_ages_no_crash(s):
    try:
        result = parse_group_ages(s)
    except Exception as e:
        assert False, f"parse_group_ages crashed on {s!r} with: {type(e).__name__}: {e}"
    # Property: result is None (rejected) or a list of realistic ages
    assert result is None or (
        isinstance(result, list) and all(isinstance(a, int) and 0 <= a <= 120 for a in result)
    ), f"parse_group_ages returned an invalid age list for {s!r}: {result!r}"


@settings(max_examples=300)
@given(date_inputs)
def test_parse_visit_date_no_crash(s):
    try:
        result = parse_visit_date(s)
    except Exception as e:
        assert False, f"parse_visit_date crashed on {s!r} with: {type(e).__name__}: {e}"
    # Property: result is None (rejected) or a real calendar date
    if result is not None:
        import datetime
        y, m, d = result
        datetime.date(y, m, d)  # must not raise -> date actually exists
