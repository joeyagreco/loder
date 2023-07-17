import unittest

from loder.model.Settings import Settings


class TestLoader(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_reset(self):
        Settings.os_env_prefix = "foo"
        Settings.env_var_absolute_file_paths = ["foo", "bar", "baz"]
        self.assertEqual("foo", Settings.os_env_prefix)
        Settings.reset()
        self.assertIsNone(Settings.os_env_prefix)
        self.assertEqual([], Settings.env_var_absolute_file_paths)
