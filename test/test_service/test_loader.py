import os
import unittest
from loder.enumeration.EnvVarSource import EnvVarSource
from loder.model.EnvData import EnvData

from loder.model.EnvVarMemory import EnvVarMemory
from loder.model.Settings import Settings
from loder.service import loader
from unittest.mock import patch


class TestLoader(unittest.TestCase):
    def setUp(self):
        # Store the original environment variables
        self.original_environ = dict(os.environ)
        # Clear all environment variables
        os.environ.clear()

        EnvVarMemory.env_vars = {}
        EnvVarMemory.env_vars_unprocessed = {}

    def tearDown(self):
        # Restore original environment variables after test
        os.environ.clear()
        os.environ.update(self.original_environ)

    def test_define_happyPath(self):
        loader.define(key="foo", as_type=int, default_value=17, description="foo description")

        self.assertEqual({}, EnvVarMemory.env_vars)
        self.assertEqual(
            {
                "foo": EnvData(
                    as_type=int,
                    description="foo description",
                    env_var_source=EnvVarSource.CODE,
                    value=17,
                )
            },
            EnvVarMemory.env_vars_unprocessed,
        )

    @patch("os.environ")
    def test_defineAndProcess_codeVarsOnly_happyPath(self, mock_os_environ):
        loader.define(key="foo", as_type=int, default_value=17, description="foo description")
        loader.process()

        self.assertEqual({}, EnvVarMemory.env_vars_unprocessed)
        self.assertEqual(
            {
                "FOO": EnvData(
                    as_type=int,
                    description="foo description",
                    env_var_source=EnvVarSource.CODE,
                    value=17,
                )
            },
            EnvVarMemory.env_vars,
        )

    @patch("os.environ")
    def test_defineAndProcess_fileVarsOnly_happyPath(self, mock_os_environ):
        # JSON
        cwd = os.path.abspath(os.getcwd())
        json_file_path = os.path.join(cwd, "resource", "dummy_1.json")

        Settings.env_var_absolute_file_paths = [json_file_path]
        loader.process()

        self.assertEqual({}, EnvVarMemory.env_vars_unprocessed)
        self.assertEqual(
            {
                "FOO": EnvData(
                    as_type=str, description="", env_var_source=EnvVarSource.FILE, value="foo"
                ),
                "BAR": EnvData(
                    as_type=str, description="", env_var_source=EnvVarSource.FILE, value="BAR"
                ),
                "BAZ": EnvData(
                    as_type=str, description="", env_var_source=EnvVarSource.FILE, value="baz"
                ),
            },
            EnvVarMemory.env_vars,
        )
