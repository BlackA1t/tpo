# test_calculator.py
import pytest
from calculator import Calculator

class TestCalculator:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.calc = Calculator()

    # --- Тесты для метода ADD ---
    
    # Простой тест
    def test_add_simple(self):
        assert self.calc.add(2, 3) == 5

    # Параметризованный тест
    @pytest.mark.parametrize("a, b, expected", [
        (10, 5, 15),       # положительные
        (-1, 1, 0),        # отрицательное и положительное
        (-5, -5, -10),     # отрицательные
        (0, 0, 0),         # нули
        (1.5, 2.5, 4.0)    # дробные
    ])
    def test_add_parametrized(self, a, b, expected):
        assert self.calc.add(a, b) == expected

    # --- Тесты для метода DIVIDE ---

    def test_divide_simple(self):
        assert self.calc.divide(10, 2) == 5

    def test_divide_float(self):
        assert self.calc.divide(5, 2) == 2.5

    # Тест на вызов исключения
    def test_divide_by_zero(self):
        with pytest.raises(ValueError) as exc_info:
            self.calc.divide(10, 0)
        assert str(exc_info.value) == "Делить на ноль нельзя"

    # --- Тесты для метода IS_PRIME_NUMBER ---

    @pytest.mark.parametrize("number, expected", [
        (2, True),
        (3, True),
        (4, False),
        (5, True),
        (9, False),
        (13, True),
        (1, False),
        (0, False),
        (-5, False),
        (100, False)
    ])
    def test_is_prime_parametrized(self, number, expected):
        assert self.calc.is_prime_number(number) == expected
