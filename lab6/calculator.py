class Calculator:
    def add(self, a, b):
        """Возвращает сумму двух чисел."""
        return a + b

    def divide(self, a, b):
        """Возвращает результат деления a на b.
        Вызывает ValueError при попытке деления на ноль.
        """
        if b == 0:
            raise ValueError("Делить на ноль нельзя")
        return a / b

    def is_prime_number(self, n):
        """Проверяет, является ли число простым.
        Возвращает True, если число простое, иначе False.
        Обрабатывает только положительные целые числа > 1.
        """
        if not isinstance(n, int) or n < 2:
            return False
        
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True
