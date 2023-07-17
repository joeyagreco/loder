import unittest
from loder.enumeration.EnvVarSource import EnvVarSource
from loder.model.EnvData import EnvData

from loder.model.EnvVarMemory import EnvVarMemory
from loder.service import loader


class TestLoader(unittest.TestCase):
    def setUp(self):
        EnvVarMemory.env_vars = {}
        EnvVarMemory.env_vars_unprocessed = {}

    def test_define_allValues_happyPath(self):
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
