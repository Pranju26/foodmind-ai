ACTIVITY_MULTIPLIERS = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
    "very_active": 1.9,
}

GOAL_ADJUSTMENTS = {
    "weight_loss": -500,
    "weight_gain": 500,
    "muscle_gain": 300,
    "maintain": 0,
}


def calculate_bmr(sex: str, weight_kg: float, height_cm: float, age: int) -> float:
    base = (10 * weight_kg) + (6.25 * height_cm) - (5 * age)
    if sex == "male":
        return base + 5
    else:
        return base - 5


def calculate_tdee(bmr: float, activity_level: str) -> float:
    multiplier = ACTIVITY_MULTIPLIERS.get(activity_level, 1.2)
    return bmr * multiplier


def calculate_calorie_target(tdee: float, goal: str) -> float:
    adjustment = GOAL_ADJUSTMENTS.get(goal, 0)
    return tdee + adjustment


def calculate_macros(calorie_target: float, weight_kg: float) -> dict:
    protein_grams = round(weight_kg * 1.8, 1)
    protein_calories = protein_grams * 4

    fat_calories = calorie_target * 0.25
    fat_grams = round(fat_calories / 9, 1)

    remaining_calories = calorie_target - protein_calories - fat_calories
    carb_grams = round(max(remaining_calories, 0) / 4, 1)

    return {
        "protein_grams": protein_grams,
        "fat_grams": fat_grams,
        "carb_grams": carb_grams,
    }


def calculate_full_nutrition_targets(sex: str, weight_kg: float, height_cm: float, age: int, activity_level: str, goal: str) -> dict:
    bmr = calculate_bmr(sex, weight_kg, height_cm, age)
    tdee = calculate_tdee(bmr, activity_level)
    calorie_target = calculate_calorie_target(tdee, goal)
    macros = calculate_macros(calorie_target, weight_kg)

    return {
        "bmr": round(bmr, 1),
        "tdee": round(tdee, 1),
        "calorie_target": round(calorie_target, 1),
        "protein_grams": macros["protein_grams"],
        "fat_grams": macros["fat_grams"],
        "carb_grams": macros["carb_grams"],
    }
