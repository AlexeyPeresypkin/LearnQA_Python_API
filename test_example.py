class TestExample:
    def test_check_math(self):
        a = 5
        b = 9
        assert a + b == 14

    def test_check_math1(self):
        a = 51
        b = 9
        expected_sum = 60
        assert a + b == expected_sum, f'Sum of variables a and b is not equal to {expected_sum}'
