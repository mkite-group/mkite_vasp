import unittest as ut
from unittest.mock import patch

from custodian.vasp.jobs import VaspJob
from mkite_vasp.runners import VaspRunner
from mkite_vasp.settings import VaspSettings


class TestRunner(ut.TestCase):
    def setUp(self):
        self.settings = VaspSettings()
        self.runner = VaspRunner(self.settings)

    def test_cmd(self):
        cmd = self.runner.cmd
        expected = ["vasp_std"]

        self.assertEqual(cmd, expected)

    def test_create_jobs(self):
        jobs = self.runner.create_jobs()
        self.assertIsInstance(jobs, list)
        self.assertIsInstance(jobs[0], VaspJob)

    @patch("mkite_vasp.recipes.vasp.runner.Custodian")
    def test_run(self, mock_custodian):
        self.runner.run()
        self.assertTrue(mock_custodian.called)

