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

        EnvVarMemory.reset()
        Settings.reset()

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
    def test_defineAndProcess_fileVarsOnly_json_happyPath(self, mock_os_environ):
        cwd = os.path.dirname(os.path.abspath(__file__))
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

    @patch("os.environ")
    def test_defineAndProcess_fileVarsOnly_yaml_happyPath(self, mock_os_environ):
        cwd = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(cwd, "resource", "dummy_1.yaml")

        Settings.env_var_absolute_file_paths = [json_file_path]
        loader.process()

        self.assertEqual({}, EnvVarMemory.env_vars_unprocessed)
        self.assertEqual(
            {
                "FOO": EnvData(
                    as_type=str, description="", env_var_source=EnvVarSource.FILE, value="foo"
                ),
                "BAR": EnvData(
                    as_type=int, description="", env_var_source=EnvVarSource.FILE, value=1
                ),
                "BAZ": EnvData(
                    as_type=float, description="", env_var_source=EnvVarSource.FILE, value=1.1
                ),
                "BOT": EnvData(
                    as_type=bool, description="", env_var_source=EnvVarSource.FILE, value=True
                ),
            },
            EnvVarMemory.env_vars,
        )

    @patch("os.environ")
    def test_defineAndProcess_fileVarsOnly_yml_happyPath(self, mock_os_environ):
        cwd = os.path.dirname(os.path.abspath(__file__))
        json_file_path = os.path.join(cwd, "resource", "dummy_1.yml")

        Settings.env_var_absolute_file_paths = [json_file_path]
        loader.process()

        self.assertEqual({}, EnvVarMemory.env_vars_unprocessed)
        self.assertEqual(
            {
                "FOO": EnvData(
                    as_type=str, description="", env_var_source=EnvVarSource.FILE, value="foo"
                ),
                "BAR": EnvData(
                    as_type=int, description="", env_var_source=EnvVarSource.FILE, value=2
                ),
                "BAZ": EnvData(
                    as_type=float, description="", env_var_source=EnvVarSource.FILE, value=2.2
                ),
                "BOT": EnvData(
                    as_type=bool, description="", env_var_source=EnvVarSource.FILE, value=True
                ),
            },
            EnvVarMemory.env_vars,
        )

    @patch.dict(
        "os.environ", {"foo": "a", "bar": "b"}
    )  # this seems to be the only way to mock os.environ
    @patch("loder.service.loader.load_dotenv")
    def test_defineAndProcess_osVarsOnly_yml_happyPath(self, mock_load_dotenv):
        loader.process()
        EnvVarMemory.print()

        self.assertEqual({}, EnvVarMemory.env_vars_unprocessed)
        self.assertEqual(
            {
                "FOO": EnvData(
                    as_type=str, description="", env_var_source=EnvVarSource.OS, value="a"
                ),
                "BAR": EnvData(
                    as_type=str, description="", env_var_source=EnvVarSource.OS, value="b"
                ),
            },
            EnvVarMemory.env_vars,
        )
