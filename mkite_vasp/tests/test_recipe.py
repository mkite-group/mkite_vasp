import os
import warnings
import unittest as ut
from unittest.mock import Mock
from pkg_resources import resource_filename

from mkite_core.models import JobInfo
from mkite_core.recipes.runner import BaseRunner
from mkite_vasp.recipes import VaspRecipe
from mkite_core.tests.tempdirs import run_in_tempdir


INFO = JobInfo.from_json(resource_filename("mkite_core.tests.files", "jobinfo.json"))


class MockRunner(BaseRunner):
    def cmd(self):
        return "echo vasp"

    def run(self):
        return self.cmd


class MockVaspRecipe(VaspRecipe):
    RUNNER_CLS = MockRunner


class TestRecipe(ut.TestCase):
    def get_recipe(self):
        return MockVaspRecipe(INFO)

    def test_creation(self):
        recipe = self.get_recipe()
        self.assertTrue(hasattr(recipe, "SETTINGS_CLS"))
        self.assertTrue(hasattr(recipe, "OPTIONS"))

    @run_in_tempdir
    def test_setup(self):
        workdir = "."
        recipe = self.get_recipe()

        # ignores pymatgen warnings on the wrong POTCARs
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            recipe.setup(workdir)

        files = set(os.listdir(workdir))
        expected = {"INCAR", "POSCAR", "KPOINTS", "POTCAR"}

        self.assertEqual(files, expected)

    def test_options(self):
        recipe = self.get_recipe()
        opts = recipe.get_options()

        self.assertEqual(opts["INCAR"]["ENCUT"], 680)

    def test_inputs(self):
        from pymatgen.core import Structure
        recipe = self.get_recipe()
        inp = recipe.get_inputs()

        self.assertTrue(isinstance(inp, Structure))

    def test_run(self):
        recipe = self.get_recipe()
        cmd = recipe.run_job()
        self.assertEqual(cmd, ["vasp_std"])

    @run_in_tempdir
    def test_setup_workdir(self):
        workdir = "./test"
        recipe = self.get_recipe()

        # ignores pymatgen warnings on the wrong POTCARs
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            recipe.setup(workdir)
