from app.services.nutrition_engine import (
    calculate_bmr,
    calculate_tdee,
    calculate_calorie_target,
    calculate_macros,
)


def test_calculate_bmr_male():
    # Using the exact numbers from Step 39: male, 70kg, 175cm, 22yo
    result = calculate_bmr(sex="male", weight_kg=70, height_cm=175, age=22)
    assert round(result, 2) == 1688.75


def test_calculate_bmr_female():
    result = calculate_bmr(sex="female", weight_kg=60, height_cm=165, age=30)
    expected = (10 * 60) + (6.25 * 165) - (5 * 30) - 5
    assert round(result, 2) == round(expected, 2)


def test_calculate_tdee_moderate_activity():
    bmr = 1688.75
    result = calculate_tdee(bmr, "moderate")
    assert round(result, 2) == round(bmr * 1.55, 2)


def test_calculate_tdee_sedentary_is_lowest():
    bmr = 1500
    sedentary = calculate_tdee(bmr, "sedentary")
    very_active = calculate_tdee(bmr, "very_active")
    assert sedentary < very_active


def test_calculate_calorie_target_weight_loss():
    tdee = 2500
    result = calculate_calorie_target(tdee, "weight_loss")
    assert result == 2000


def test_calculate_calorie_target_muscle_gain():
    tdee = 2617.5625
    result = calculate_calorie_target(tdee, "muscle_gain")
    assert result == tdee + 300


def test_calculate_macros_protein_scales_with_weight():
    macros_light = calculate_macros(calorie_target=2000, weight_kg=60)
    macros_heavy = calculate_macros(calorie_target=2000, weight_kg=90)
    assert macros_heavy["protein_grams"] > macros_light["protein_grams"]


def test_calculate_macros_no_negative_values():
    macros = calculate_macros(calorie_target=1200, weight_kg=100)
    assert macros["protein_grams"] >= 0
    assert macros["fat_grams"] >= 0
    assert macros["carb_grams"] >= 0
