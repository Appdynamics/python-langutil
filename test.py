from langutil import php
import unittest


class TestPHPScalarStringGeneratorFunctions(unittest.TestCase):
    def test_generate_scalar_int(self):
        self.assertEqual(php.generate_scalar(2), '2')

    def test_generate_scalar_float(self):
        self.assertEqual(php.generate_scalar(2.001), '2.001')

    def test_generate_scalar_bools(self):
        self.assertEqual(php.generate_scalar(True), 'TRUE')
        self.assertEqual(php.generate_scalar(False), 'FALSE')
        self.assertEqual(php.generate_scalar(True, upper_keywords=False),
                         'true')
        self.assertEqual(php.generate_scalar(False, upper_keywords=False),
                         'false')

    def test_generate_scalar_null(self):
        self.assertEqual(php.generate_scalar(None), 'NULL')
        self.assertEqual(php.generate_scalar(None, upper_keywords=False),
                         'null')

    def test_nonspecial_string(self):
        self.assertEqual(php.generate_scalar('non-special string'),
                         "'non-special string'")

    def test_special_string(self):
        self.assertEqual(php.generate_scalar('special\nstring'),
                         '"special\nstring"')
        self.assertEqual(php.generate_scalar('special\rstring'),
                         '"special\rstring"')
        self.assertEqual(php.generate_scalar('\tspecial\rstring'),
                         '"\tspecial\rstring"')

    def _raises_exception_cb(self):
        php.generate_scalar([])

    def test_nonacceptable_type(self):
        self.assertRaises(php.PHPScalarException, self._raises_exception_cb)


class TestPHPArrayStringGeneratorFunction(unittest.TestCase):
    def test_generate_simple_array_from_list(self):
        expected_ret = """array(
  1,
  2,
  3,
);"""
        ret = php.generate_array([1, 2, 3])
        self.assertEqual(expected_ret, php.generate_array([1, 2, 3]))

    def test_generate_many_lists_recursive_to_array(self):
        expected_ret = """array(
    1,
    array(
        3,
        4,
    ),
    2,
    array(
        5,
        6,
    ),
);"""
        ret = php.generate_array([1, [3, 4], 2, [5, 6]], indent=4)
        self.assertEqual(expected_ret, ret)

    def test_generate_simple_dict_to_array(self):
        expected_ret = """array(
    'a' => 2,
    'b' => 3,
);"""
        ret = php.generate_array({'a': 2, 'b': 3}, indent=4)
        self.assertEqual(expected_ret, ret)

    def test_dict_to_array_recursive(self):
        expected_ret = """array(
    'b' => array(
        1,
        2,
        array(
            "key\n" => "special\tstring",
            'non' => 'special string',
        ),
    ),
    'c' => 2,
    'd' => array(
        array(
            array(
            ),
        ),
    ),
);"""
        python_val = {
            'b': [
                1,
                2,
                {
                    'key\n': 'special\tstring',
                    'non': 'special string',
                    '_order': ['key\n', 'non'],
                },
            ],
            'c': 2,
            'd': [[{}]],
            '_order': ['b', 'c', 'd'],
        }
        ret = php.generate_array(python_val, indent=4)
        self.assertEqual(expected_ret, ret)


class TestPHPSerialize(unittest.TestCase):
    def test_serialize(self):
        self.assertNotEqual(php.serialize([]), [])

    def test_unserialize(self):
        self.assertEqual(php.unserialize('a:0:{};'), {})

# This is used to keep compatibility with 2.6
if __name__ == '__main__':
    unittest.main()
