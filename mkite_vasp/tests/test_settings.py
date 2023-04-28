import unittest as ut
from mkite_vasp.settings import VaspOptions, VaspSettings


class TestOptions(ut.TestCase):
    def test_creation(self):
        opts = VaspOptions.get_defaults()
        self.assertTrue(hasattr(opts, "INCAR"))
        self.assertEqual(opts.INCAR["ALGO"], "Fast")


class TestSettings(ut.TestCase):
    def test_creation(self):
        settings = VaspSettings()
        self.assertTrue(hasattr(settings, "VASP_DEFAULT_OPTIONS"))
        self.assertTrue(hasattr(settings, "VASP_STD"))
