"""
Lab 6 - Code (Line/Statement) Coverage tests for museum_admission.py
Goal: execute every statement in the module at least once (>= 90% line coverage).

Run:
    coverage run -m pytest CodeCoverageTest_museum_admission.py
    coverage report -m
"""
import pytest
from museum_admission import ticket_price, group_discount, gallery_entry


# ---------------- ticket_price ----------------

def test_adult_weekday():
    assert ticket_price("adult", 30, "tuesday", False) == 300


def test_unknown_category_raises():
    with pytest.raises(ValueError, match="unknown category"):
        ticket_price("vip", 30, "tuesday", False)


def test_negative_age_raises():
    with pytest.raises(ValueError, match="invalid age"):
        ticket_price("adult", -1, "tuesday", False)


def test_toddler_enters_free():
    assert ticket_price("child", 3, "saturday", True) == 0


def test_monday_half_price():
    assert ticket_price("adult", 30, "monday", False) == 150


def test_weekend_surcharge():
    assert ticket_price("senior", 70, "saturday", False) == 250


def test_student_guided_tour():
    assert ticket_price("student", 20, "tuesday", True) == 200


def test_adult_guided_tour():
    assert ticket_price("adult", 40, "wednesday", True) == 400


# ---------------- group_discount ----------------

def test_small_group():
    assert group_discount(4, False) == 0


def test_invalid_group_size_raises():
    with pytest.raises(ValueError, match="invalid group size"):
        group_discount(0, False)


def test_large_school_group():
    assert group_discount(25, True) == 40


def test_small_school_group():
    assert group_discount(10, True) == 25


def test_large_public_group():
    assert group_discount(15, False) == 20


def test_medium_public_group():
    assert group_discount(8, False) == 10


# ---------------- gallery_entry ----------------

def test_gallery_full_wait():
    assert gallery_entry(100, 100, True) == "wait"


def test_gallery_nearly_full_queue():
    assert gallery_entry(95, 100, False) == "queue"


def test_gallery_enter():
    assert gallery_entry(10, 100, False) == "enter"
