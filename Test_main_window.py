from main_window import *
import unittest
import os


class Test_TextAln(unittest.TestCase):
    def setUp(self):
        self.TextBox = TextManipStuff()

    def test_BulletWStr(self):
        self.assertLess(len("text"), len(
            self.TextBox.make_bullet_format("text")))

    def test_NumberWStr(self):
        self.assertLess(len("text"), len(
            self.TextBox.make_bullet_format("text")))

    def test_BulletWBlank(self):
        self.assertLess(len(""), len(
            self.TextBox.make_bullet_format("")))

    def test_NumberWBlank(self):
        self.assertLess(len("text"), len(
            self.TextBox.make_bullet_format("")))

    def test_BulletCorrectFlags(self):
        self.assertEqual("<ul><li>Hi dude</li></ul>",
                         self.TextBox.make_bullet_format("Hi dude"))

    def test_NumberedCorrectFlags(self):
        self.assertEqual("<ol><li>Hi dude</li></ol>",
                         self.TextBox.make_numbered_format("Hi dude"))


class Test_Contants(unittest.TestCase):
    def test_FONT_SIZESvalues(self):
        self.assertEqual([5, 5.5, 6.5, 7.5, 8, 9, 10, 10.5, 11, 12,
                          14, 16, 18, 20, 22, 24, 26, 28, 36, 48, 72], FONT_SIZES)

    def test_FONT_COLORSvalues(self):
        self.assertEqual(["Black", "Red", "Green", "Blue",
                          "Yellow", "Gray", "Magenta"], FONT_COLORS)


class Test_CutStr(unittest.TestCase):
    def setUp(self):
        self.String = CutStr()

    def test_snip10_gr(self):
        self.assertGreater(len("This be mah string"), len(
            self.String.snip10("This be mah string")))

    def test_snip10_eq(self):
        self.assertEqual(len(self.String.snip10(
            "This has nums 0123456789")), len("This had nums "))
