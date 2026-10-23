"""
Unit tests for nutrition calculation utilities
Tests BMI, BMR, TDEE, and macronutrient calculations
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils import nutrition as nutr


class TestBMICalculation:
    """Test BMI calculation functions"""
    
    def test_normal_bmi(self):
        """Test normal BMI calculation"""
        bmi = nutr.calculate_bmi(70, 175)
        assert 22.0 <= bmi <= 23.0
    
    def test_underweight_bmi(self):
        """Test underweight BMI"""
        bmi = nutr.calculate_bmi(50, 175)
        category = nutr.get_bmi_category(bmi)
        assert category == "Underweight"
    
    def test_overweight_bmi(self):
        """Test overweight BMI"""
        bmi = nutr.calculate_bmi(90, 175)
        category = nutr.get_bmi_category(bmi)
        assert category in ["Overweight", "Obese"]
    
    def test_zero_values(self):
        """Test BMI with zero values"""
        bmi = nutr.calculate_bmi(0, 175)
        assert bmi == 0
        
        bmi = nutr.calculate_bmi(70, 0)
        assert bmi == 0


class TestBMRCalculation:
    """Test BMR calculation functions"""
    
    def test_male_bmr(self):
        """Test BMR calculation for males"""
        bmr = nutr.calculate_bmr(70, 175, 30, 'male')
        assert 1600 <= bmr <= 1800
    
    def test_female_bmr(self):
        """Test BMR calculation for females"""
        bmr = nutr.calculate_bmr(60, 165, 30, 'female')
        assert 1300 <= bmr <= 1500
    
    def test_age_impact(self):
        """Test that age affects BMR"""
        bmr_young = nutr.calculate_bmr(70, 175, 20, 'male')
        bmr_old = nutr.calculate_bmr(70, 175, 60, 'male')
        assert bmr_young > bmr_old
    
    def test_zero_values(self):
        """Test BMR with zero values"""
        bmr = nutr.calculate_bmr(0, 175, 30, 'male')
        assert bmr == 0


class TestTDEECalculation:
    """Test TDEE calculation functions"""
    
    def test_sedentary_tdee(self):
        """Test TDEE for sedentary activity"""
        bmr = 1700
        tdee = nutr.calculate_tdee(bmr, 'sedentary')
        assert tdee == bmr * 1.2
    
    def test_very_active_tdee(self):
        """Test TDEE for very active lifestyle"""
        bmr = 1700
        tdee = nutr.calculate_tdee(bmr, 'very_active')
        assert tdee == bmr * 1.725
    
    def test_activity_levels(self):
        """Test that higher activity = higher TDEE"""
        bmr = 1700
        tdee_sed = nutr.calculate_tdee(bmr, 'sedentary')
        tdee_active = nutr.calculate_tdee(bmr, 'very_active')
        assert tdee_active > tdee_sed


class TestCalorieTarget:
    """Test calorie target calculations"""
    
    def test_maintain_weight(self):
        """Test calorie target for weight maintenance"""
        tdee = 2000
        target = nutr.calculate_calorie_target(tdee, 'maintain')
        assert target == tdee
    
    def test_lose_weight(self):
        """Test calorie target for weight loss"""
        tdee = 2000
        target = nutr.calculate_calorie_target(tdee, 'lose')
        assert target == tdee - 500
    
    def test_gain_weight(self):
        """Test calorie target for weight gain"""
        tdee = 2000
        target = nutr.calculate_calorie_target(tdee, 'gain')
        assert target == tdee + 500
    
    def test_minimum_calories(self):
        """Test minimum calorie floor"""
        tdee = 1000
        target = nutr.calculate_calorie_target(tdee, 'lose')
        assert target >= 1200


class TestMacronutrientTargets:
    """Test macronutrient target calculations"""
    
    def test_balanced_macros(self):
        """Test balanced macronutrient distribution"""
        target = 2000
        macros = nutr.calculate_macronutrient_targets(target, 'balanced')
        
        # Check that all macros are positive
        assert macros['protein'] > 0
        assert macros['carbs'] > 0
        assert macros['fat'] > 0
        
        # Verify approximate calorie match
        protein_cal = macros['protein'] * 4
        carbs_cal = macros['carbs'] * 4
        fat_cal = macros['fat'] * 9
        total_cal = protein_cal + carbs_cal + fat_cal
        
        # Allow 10% variance
        assert abs(total_cal - target) <= target * 0.1
    
    def test_weight_loss_macros(self):
        """Test macros for weight loss (higher protein)"""
        target = 2000
        macros_loss = nutr.calculate_macronutrient_targets(target, 'lose')
        macros_balanced = nutr.calculate_macronutrient_targets(target, 'balanced')
        
        # Weight loss should have higher protein percentage
        assert macros_loss['protein'] >= macros_balanced['protein']


class TestWaterTarget:
    """Test water intake target calculations"""
    
    def test_basic_water_target(self):
        """Test basic water calculation"""
        water = nutr.calculate_water_target(70, 'moderately_active')
        assert 2.0 <= water <= 3.5
    
    def test_activity_impact(self):
        """Test that activity level affects water target"""
        water_sed = nutr.calculate_water_target(70, 'sedentary')
        water_active = nutr.calculate_water_target(70, 'very_active')
        assert water_active > water_sed
    
    def test_weight_impact(self):
        """Test that weight affects water target"""
        water_light = nutr.calculate_water_target(50, 'moderately_active')
        water_heavy = nutr.calculate_water_target(90, 'moderately_active')
        assert water_heavy > water_light


class TestNutritionScaling:
    """Test nutrition value scaling"""
    
    def test_scale_up(self):
        """Test scaling nutrition values up"""
        nutrition = {
            'calories': 100,
            'protein': 10,
            'carbohydrates': 15,
            'fat': 5,
            'fiber': 2
        }
        
        scaled = nutr.scale_nutrition_values(nutrition, 2.0)
        
        assert scaled['calories'] == 200
        assert scaled['protein'] == 20
        assert scaled['carbohydrates'] == 30
        assert scaled['fat'] == 10
        assert scaled['fiber'] == 4
    
    def test_scale_down(self):
        """Test scaling nutrition values down"""
        nutrition = {
            'calories': 100,
            'protein': 10,
            'carbohydrates': 15,
            'fat': 5,
            'fiber': 2
        }
        
        scaled = nutr.scale_nutrition_values(nutrition, 0.5)
        
        assert scaled['calories'] == 50
        assert scaled['protein'] == 5
        assert scaled['carbohydrates'] == 7.5
        assert scaled['fat'] == 2.5
        assert scaled['fiber'] == 1


# Run tests
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
