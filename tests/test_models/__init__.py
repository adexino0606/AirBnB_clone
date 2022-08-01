#!/usr/bin/python3
"""This file defines tests cases for the __init__"""
import unittest
import pycodestyle


class Test___Init__(unittest.TestCase):
    """
    Tests for __init__.py
    """

    # Test for Documentation

    def test_pep8_base(self):
        """
        Test that checks PEP8 | Pycodestyle
        """
        syntax = pycodestyle.StyleGuide(quit=True)
        check = syntax.check_files(['models/__init__.py'])
        self.assertEqual(
            check.total_errors, 0,
            "Found code style error (and warnings)"
        )
