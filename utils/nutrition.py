"""
Nutrition calculation utilities for FoodMind AI
Implements BMI, BMR, TDEE, and macronutrient calculations
"""

def calculate_bmi(weight_kg, height_cm):
    """
    Calculate Body Mass Index (BMI)
    
    Formula: BMI = weight(kg) / (height(m))^2
    
    Args:
        weight_kg: Weight in kilograms
        height_cm: Height in centimeters
    
    Returns:
        BMI value
    """
    if height_cm <= 0 or weight_kg <= 0:
        return 0
    
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    return round(bmi, 1)


def get_bmi_category(bmi):
    """
    Get BMI category based on WHO standards
    
    Args:
        bmi: BMI value
    
    Returns:
        BMI category string
    """
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def calculate_bmr(weight_kg, height_cm, age, gender='male'):
    """
    Calculate Basal Metabolic Rate (BMR) using Mifflin-St Jeor Equation
    
    Formula:
    - Men: BMR = 10 * weight(kg) + 6.25 * height(cm) - 5 * age + 5
    - Women: BMR = 10 * weight(kg) + 6.25 * height(cm) - 5 * age - 161
    
    Args:
        weight_kg: Weight in kilograms
        height_cm: Height in centimeters
        age: Age in years
        gender: 'male' or 'female'
    
    Returns:
        BMR in calories/day
    """
    if weight_kg <= 0 or height_cm <= 0 or age <= 0:
        return 0
    
    bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age
    
    if gender.lower() == 'male':
        bmr += 5
    else:
        bmr -= 161
    
    return round(bmr, 0)


def calculate_tdee(bmr, activity_level):
    """
    Calculate Total Daily Energy Expenditure (TDEE)
    
    Activity multipliers:
    - sedentary: 1.2 (little or no exercise)
    - lightly_active: 1.375 (exercise 1-3 days/week)
    - moderately_active: 1.55 (exercise 3-5 days/week)
    - very_active: 1.725 (exercise 6-7 days/week)
    - extremely_active: 1.9 (physical job or training twice/day)
    
    Args:
        bmr: Basal Metabolic Rate
        activity_level: Activity level string
    
    Returns:
        TDEE in calories/day
    """
    activity_multipliers = {
        'sedentary': 1.2,
        'lightly_active': 1.375,
        'moderately_active': 1.55,
        'very_active': 1.725,
        'extremely_active': 1.9
    }
    
    multiplier = activity_multipliers.get(activity_level, 1.2)
    tdee = bmr * multiplier
    
    return round(tdee, 0)


def calculate_calorie_target(tdee, goal):
    """
    Calculate daily calorie target based on nutrition goal
    
    Goals:
    - maintain: TDEE (no change)
    - lose: TDEE - 500 (approximately 0.5kg loss per week)
    - gain: TDEE + 500 (approximately 0.5kg gain per week)
    - balanced: TDEE
    
    Args:
        tdee: Total Daily Energy Expenditure
        goal: Nutrition goal string
    
    Returns:
        Target calories/day
    """
    adjustments = {
        'maintain': 0,
        'lose': -500,
        'gain': 500,
        'balanced': 0
    }
    
    adjustment = adjustments.get(goal, 0)
    target = tdee + adjustment
    
    # Ensure minimum calorie intake
    return max(1200, round(target, 0))


def calculate_macronutrient_targets(calorie_target, goal='balanced'):
    """
    Calculate macronutrient targets based on calorie target and goal
    
    Standard distribution:
    - Protein: 25-30% of calories (4 cal/g)
    - Carbs: 40-50% of calories (4 cal/g)
    - Fat: 25-30% of calories (9 cal/g)
    
    Args:
        calorie_target: Daily calorie target
        goal: Nutrition goal (affects distribution)
    
    Returns:
        Dictionary with protein, carbs, fat in grams
    """
    if goal == 'lose':
        # Higher protein for weight loss
        protein_percent = 0.30
        carbs_percent = 0.40
        fat_percent = 0.30
    elif goal == 'gain':
        # Higher carbs for weight gain
        protein_percent = 0.25
        carbs_percent = 0.50
        fat_percent = 0.25
    else:
        # Balanced distribution
        protein_percent = 0.25
        carbs_percent = 0.45
        fat_percent = 0.30
    
    protein_g = (calorie_target * protein_percent) / 4
    carbs_g = (calorie_target * carbs_percent) / 4
    fat_g = (calorie_target * fat_percent) / 9
    
    return {
        'protein': round(protein_g, 1),
        'carbs': round(carbs_g, 1),
        'fat': round(fat_g, 1)
    }


def calculate_water_target(weight_kg, activity_level='moderately_active'):
    """
    Calculate daily water intake target
    
    Base formula: 30-35ml per kg of body weight
    Adjusted for activity level
    
    Args:
        weight_kg: Weight in kilograms
        activity_level: Activity level string
    
    Returns:
        Water target in liters
    """
    if weight_kg <= 0:
        return 0
    
    # Base calculation: 33ml per kg
    base_water_ml = weight_kg * 33
    
    # Activity adjustments
    activity_adjustments = {
        'sedentary': 1.0,
        'lightly_active': 1.1,
        'moderately_active': 1.2,
        'very_active': 1.3,
        'extremely_active': 1.4
    }
    
    multiplier = activity_adjustments.get(activity_level, 1.2)
    water_ml = base_water_ml * multiplier
    water_liters = water_ml / 1000
    
    return round(water_liters, 1)


def scale_nutrition_values(nutrition_data, multiplier):
    """
    Scale nutrition values by a multiplier (for serving adjustments)
    
    Args:
        nutrition_data: Dictionary with nutrition values
        multiplier: Multiplication factor
    
    Returns:
        Scaled nutrition dictionary
    """
    return {
        'calories': round(nutrition_data.get('calories', 0) * multiplier, 1),
        'protein': round(nutrition_data.get('protein', 0) * multiplier, 1),
        'carbohydrates': round(nutrition_data.get('carbohydrates', 0) * multiplier, 1),
        'fat': round(nutrition_data.get('fat', 0) * multiplier, 1),
        'fiber': round(nutrition_data.get('fiber', 0) * multiplier, 1)
    }
