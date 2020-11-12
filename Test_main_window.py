"""Unit tests for string manipulation and constant variable values from main_window"""

from main_window import *
import unittest


class Test_StrManip(unittest.TestCase):
    """Test string manipulations"""

    # Init
    def setUp(self):
        self.TextBox = TextManipStuff()

    # Should return string with bulleted list tags in html (greater length)
    def test_BulletWStr(self):
        self.assertLess(len("text"), len(
            self.TextBox.make_bullet_format("text")))

    # Should return string with numbered list tags in html (greater length)
    def test_NumberWStr(self):
        self.assertLess(len("text"), len(
            self.TextBox.make_bullet_format("text")))

    # Should return bulleted list tags (greater than blank)
    def test_BulletWBlank(self):
        self.assertLess(len(""), len(
            self.TextBox.make_bullet_format("")))

    # Should return numbered list tags (greater than blank)
    def test_NumberWBlank(self):
        self.assertLess(len("text"), len(
            self.TextBox.make_bullet_format("")))

    # Test that tags are correct for bulleted list
    def test_BulletCorrectFlags(self):
        self.assertEqual("<ul><li>Hi dude</li></ul>",
                         self.TextBox.make_bullet_format("Hi dude"))

    # Test that tags are correct for numbered list
    def test_NumberedCorrectFlags(self):
        self.assertEqual("<ol><li>Hi dude</li></ol>",
                         self.TextBox.make_numbered_format("Hi dude"))


class Test_Contants(unittest.TestCase):
    """Test values of constant variables since they are defined by ranges and extensions"""

    # Enumerate each value for FONT_SIZES. Should match result of range and extend in main_window
    def test_FONT_SIZESvalues(self):
        self.assertEqual([5, 5.5, 6.5, 7.5, 8, 9, 10, 10.5, 11, 12,
                          14, 16, 18, 20, 22, 24, 26, 28, 36, 48, 72], FONT_SIZES)

    # Also test font color values
    def test_FONT_COLORSvalues(self):
        self.assertEqual(["Black", "Red", "Green", "Blue",
                          "Yellow", "Gray", "Magenta"], FONT_COLORS)


class Test_CutStr(unittest.TestCase):
    """Test strings returned by CutStr"""

    # Init
    def setUp(self):
        self.String = CutStr()

    # Snippet returned should be shorted
    def test_snip10_gr(self):
        self.assertGreater(len("This be mah string"), len(
            self.String.snip10("This be mah string")))

    # Snippet should be exactly the string except for the last 10 chars
    def test_snip10_eq(self):
        self.assertEqual(len(self.String.snip10(
            "This has nums 0123456789")), len("This had nums "))
