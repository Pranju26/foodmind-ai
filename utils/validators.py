"""
Data validation utilities for FoodMind AI
"""

def validate_profile_data(data):
    """
    Validate user profile data
    
    Args:
        data: Dictionary with profile fields
    
    Returns:
        Tuple (is_valid, error_messages)
    """
    errors = []
    
    # Name validation
    if not data.get('name') or len(data['name'].strip()) < 2:
        errors.append("Name must be at least 2 characters long")
    
    # Age validation
    age = data.get('age')
    if age is None or age <= 0 or age > 120:
        errors.append("Age must be between 1 and 120")
    
    # Height validation (in cm)
    height = data.get('height')
    if height is None or height < 50 or height > 300:
        errors.append("Height must be between 50 and 300 cm")
    
    # Weight validation (in kg)
    weight = data.get('weight')
    if weight is None or weight < 20 or weight > 300:
        errors.append("Weight must be between 20 and 300 kg")
    
    # Activity level validation
    valid_activity_levels = ['sedentary', 'lightly_active', 'moderately_active', 'very_active', 'extremely_active']
    if data.get('activity_level') not in valid_activity_levels:
        errors.append("Invalid activity level selected")
    
    # Nutrition goal validation
    valid_goals = ['maintain', 'lose', 'gain', 'balanced']
    if data.get('nutrition_goal') not in valid_goals:
        errors.append("Invalid nutrition goal selected")
    
    return len(errors) == 0, errors


def validate_meal_data(data):
    """
    Validate meal record data
    
    Args:
        data: Dictionary with meal fields
    
    Returns:
        Tuple (is_valid, error_messages)
    """
    errors = []
    
    # Food name validation
    if not data.get('food_name') or len(data['food_name'].strip()) < 2:
        errors.append("Food name must be at least 2 characters long")
    
    # Quantity validation
    quantity = data.get('quantity')
    if quantity is None or quantity <= 0 or quantity > 100:
        errors.append("Quantity must be between 0 and 100")
    
    # Meal type validation
    valid_meal_types = ['breakfast', 'lunch', 'dinner', 'snack']
    if data.get('meal_type') not in valid_meal_types:
        errors.append("Invalid meal type selected")
    
    # Nutrition values validation (should be non-negative)
    for field in ['calories', 'protein', 'carbohydrates', 'fat']:
        value = data.get(field, 0)
        if value < 0:
            errors.append(f"{field.capitalize()} cannot be negative")
    
    return len(errors) == 0, errors


def sanitize_string(text, max_length=200):
    """
    Sanitize user input string
    
    Args:
        text: Input string
        max_length: Maximum allowed length
    
    Returns:
        Sanitized string
    """
    if not text:
        return ""
    
    # Strip whitespace
    text = text.strip()
    
    # Truncate if too long
    if len(text) > max_length:
        text = text[:max_length]
    
    return text


def validate_numeric_input(value, min_val=0, max_val=None, allow_none=False):
    """
    Validate numeric input
    
    Args:
        value: Input value
        min_val: Minimum allowed value
        max_val: Maximum allowed value
        allow_none: Whether None is acceptable
    
    Returns:
        Tuple (is_valid, sanitized_value)
    """
    if value is None:
        if allow_none:
            return True, None
        return False, None
    
    try:
        value = float(value)
        
        if value < min_val:
            return False, None
        
        if max_val is not None and value > max_val:
            return False, None
        
        return True, value
    
    except (ValueError, TypeError):
        return False, None
