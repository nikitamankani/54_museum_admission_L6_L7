"""
Lab 6 - Branch Coverage tests for museum_admission.py
Goal: make every decision (if / elif / else, and/or) evaluate to BOTH True
and False at least once (>= 90% branch coverage), including boundary values.

Run:
    coverage run --branch -m pytest BranchCoverageTest_museum_admission.py
    coverage report -m
"""
import pytest
from museum_admission import ticket_price, group_discount, gallery_entry, BASE_PRICE


# =====================================================================
# ticket_price
#   D1: category not in BASE_PRICE      (T -> raise / F -> continue)
#   D2: age < 0                         (T -> raise / F -> continue)
#   D3: age < 5                         (T -> free  / F -> priced)
#   D4: day == "monday"                 (T -> half price / F -> D5)
#   D5: day in weekend                  (T -> +50 / F -> no change)
#   D6: with_guided_tour                (T -> D7 / F -> no tour fee)
#   D7: category == "student"           (T -> +50 / F -> +100)
# =====================================================================

# D1 True / False
def test_unknown_category_raises():
    with pytest.raises(ValueError, match="unknown category"):
        ticket_price("vip", 30, "tuesday", False)


def test_category_is_case_sensitive():
    with pytest.raises(ValueError):
        ticket_price("Adult", 30, "tuesday", False)


@pytest.mark.parametrize("category,expected", list(BASE_PRICE.items()))
def test_every_known_category_base_price(category, expected):
    # D1 False, D2 False, D3 False, D4 False, D5 False, D6 False
    assert ticket_price(category, 30, "tuesday", False) == expected


# D2 True / boundary
def test_negative_age_raises():
    with pytest.raises(ValueError, match="invalid age"):
        ticket_price("adult", -1, "tuesday", False)


def test_age_zero_is_valid_and_free():
    # D2 False at boundary (0), D3 True
    assert ticket_price("adult", 0, "tuesday", False) == 0


# D3 True / False boundaries
def test_age_four_is_free_even_with_tour_on_weekend():
    assert ticket_price("child", 4, "sunday", True) == 0


def test_age_five_pays():
    # D3 False at boundary (5)
    assert ticket_price("child", 5, "tuesday", False) == 100


# D4 True
def test_monday_half_price_adult():
    assert ticket_price("adult", 30, "monday", False) == 150


def test_monday_half_price_student_with_tour():
    # D4 True, D6 True, D7 True : 150//2 + 50
    assert ticket_price("student", 20, "monday", True) == 125


# D5 True (both weekend days) / False
def test_saturday_surcharge():
    assert ticket_price("senior", 70, "saturday", False) == 250


def test_sunday_surcharge_with_tour():
    # D5 True, D6 True, D7 False : 300 + 50 + 100
    assert ticket_price("adult", 30, "sunday", True) == 450


def test_weekday_no_surcharge():
    # D4 False, D5 False
    assert ticket_price("senior", 70, "friday", False) == 200


def test_day_is_case_sensitive():
    # "Monday" does not match "monday" -> D4 False, D5 False
    assert ticket_price("adult", 30, "Monday", False) == 300


# D6 / D7
def test_student_guided_tour():
    assert ticket_price("student", 20, "tuesday", True) == 200


def test_child_guided_tour():
    assert ticket_price("child", 8, "thursday", True) == 200


def test_senior_guided_tour_on_monday():
    # 200//2 + 100
    assert ticket_price("senior", 65, "monday", True) == 200


# =====================================================================
# group_discount
#   D1: group_size < 1      D2: is_school
#   D3: school & size >= 20 D4: size >= 15   D5: size >= 8
# =====================================================================

@pytest.mark.parametrize("size", [0, -5])
def test_invalid_group_size_raises(size):
    with pytest.raises(ValueError, match="invalid group size"):
        group_discount(size, False)


def test_invalid_school_group_size_raises():
    with pytest.raises(ValueError):
        group_discount(0, True)


@pytest.mark.parametrize("size,expected", [
    (1, 25),    # D1 False boundary, D3 False
    (19, 25),   # just below school threshold
    (20, 40),   # D3 True boundary
    (50, 40),
])
def test_school_group_discount(size, expected):
    assert group_discount(size, True) == expected


@pytest.mark.parametrize("size,expected", [
    (1, 0),     # D4 False, D5 False
    (7, 0),     # just below 8
    (8, 10),    # D5 True boundary
    (14, 10),   # just below 15
    (15, 20),   # D4 True boundary
    (100, 20),
])
def test_public_group_discount(size, expected):
    assert group_discount(size, False) == expected


# =====================================================================
# gallery_entry
#   D1: visitors_inside >= capacity
#   D2: visitors_inside*10 >= capacity*9  AND  not has_timed_slot
# =====================================================================

def test_gallery_full_wait():
    assert gallery_entry(100, 100, False) == "wait"


def test_gallery_over_capacity_wait_even_with_slot():
    assert gallery_entry(120, 100, True) == "wait"


def test_gallery_exactly_90_percent_no_slot_queue():
    # D2 True at boundary (90 * 10 == 100 * 9)
    assert gallery_entry(90, 100, False) == "queue"


def test_gallery_nearly_full_no_slot_queue():
    assert gallery_entry(99, 100, False) == "queue"


def test_gallery_nearly_full_with_slot_enter():
    # first operand True, second operand False -> D2 False
    assert gallery_entry(95, 100, True) == "enter"


def test_gallery_just_below_90_percent_enter():
    # first operand False -> D2 False (short-circuit)
    assert gallery_entry(89, 100, False) == "enter"


def test_gallery_empty_enter():
    assert gallery_entry(0, 100, False) == "enter"
