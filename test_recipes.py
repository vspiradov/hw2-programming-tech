"""Модуль для тестирования ингридиентов блюда"""
import pytest
from recipes import Ingredient

def test_ingredient_creation():
    """Проверка правильной инициализации атрибутов ингредиента"""
    ing = Ingredient("Мука", 500.0, "г")
    assert ing.name == "Мука"
    assert ing.quantity == 500.0
    assert ing.unit == "г"

def test_ingredient_quantity_nonnegative():
    """Проверка выброса исключения при отрицательном или нулевом количестве"""
    with pytest.raises(ValueError, match="Количество должно быть положительным"):
        Ingredient("Мука", -10.0, "г")

def test_ingredient_str():
    """Проверка строкового представления ингредиента"""
    ing = Ingredient("Мука", 500.0, "г")
    assert str(ing) == "Мука: 500.0 г"

def test_ingredient_eq():
    """Проверка равенства ингредиентов по имени и единице измерения"""
    ing1 = Ingredient("Мука", 500.0, "г")
    ing2 = Ingredient("Мука", 300.0, "г")
    ing3 = Ingredient("Сахар", 500.0, "г")
    ing4 = Ingredient("Мука", 500.0, "кг")
    # Совпадают имя и единица (количество не важно)
    assert ing1 == ing2
    # Разные имена
    assert ing1 != ing3
    # Разные единицы измерения
    assert ing1 != ing4
