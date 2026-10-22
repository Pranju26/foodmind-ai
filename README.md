# 🥗 FoodMind AI

**AI-Powered Nutrition Tracking and Analysis Platform**

FoodMind AI is a modern, user-friendly nutrition tracking application that helps you monitor food intake, analyze nutritional values, calculate calorie requirements, and receive AI-powered nutrition guidance.

---

## ✨ Features

### 📊 Dashboard
- Personalized nutrition overview
- Daily calorie tracking with goals
- Macronutrient progress (Protein, Carbs, Fat)
- Water intake monitoring
- Recent meals display
- Weekly calorie trends chart
- Quick action buttons

### 🔍 Food Analysis
- **Searchable Food Database** - 50+ common foods with detailed nutrition info
- **Category Filtering** - Browse by food category
- **Serving Calculator** - Adjust portions and see updated nutrition
- **Image Analysis** - Upload food photos for AI-powered recognition (requires API key)
- **Image Processing** - Validates and resizes images using Pillow
- **Manual Entry** - Add custom foods not in the database

### 🍽️ Meal Tracking
- Log meals by type (Breakfast, Lunch, Dinner, Snacks)
- Select from database or enter manually
- View today's meals grouped by type
- Daily nutrition summary
- Meal history with date range filtering
- Delete meals
- Export meal history to CSV

### 🤖 AI Nutrition Assistant
- Conversational AI powered by Google Gemini
- Personalized advice based on your profile and goals
- Nutrition questions and meal suggestions
- Context-aware responses using your data
- Suggested questions for quick guidance
- Chat history management

### 👤 Profile & Goals
- Personal information (name, age, height, weight)
- Activity level selection
- Dietary preferences
- Nutrition goal (maintain, lose, gain weight, balanced)
- **Automatic goal calculations:**
  - BMI (Body Mass Index)
  - BMR (Basal Metabolic Rate) - Mifflin-St Jeor Equation
  - TDEE (Total Daily Energy Expenditure)
  - Personalized calorie targets
  - Macronutrient targets
  - Water intake recommendations

### 📈 Nutrition Reports
- Daily calorie trends line chart
- Macronutrient distribution pie chart
- Protein intake tracking
- Weekly/monthly summaries
- Average daily nutrition stats
- Goal comparison metrics

---

## 🛠️ Technology Stack

### Core Technologies
- **Python 3** - Primary programming language
- **SQLite** - Local database for data persistence

### Key Python Libraries

1. **Streamlit (1.31.0)** 
   - Purpose: Web application framework
   - Usage: Creates interactive dashboard, forms, charts, and navigation
   - Why: Enables rapid development of data-driven web apps entirely in Python

2. **Pillow (10.2.0)**
   - Purpose: Image processing library (PIL)
   - Usage: Validates uploaded food images, resizes photos, converts formats
   - Why: Essential for safe image handling and processing before AI analysis

3. **Pandas (2.2.0)**
   - Purpose: Data manipulation and analysis
   - Usage: Processes food database CSV, aggregates meal records, prepares chart data, exports reports
   - Why: Powerful tools for working with structured nutrition data

4. **Matplotlib (3.8.2)**
   - Purpose: Data visualization and charting
   - Usage: Generates calorie trends, macronutrient pie charts, protein tracking graphs
   - Why: Creates publication-quality figures for nutrition insights

5. **Requests (2.31.0)**
   - Purpose: HTTP library for API calls
   - Usage: Communicates with external APIs (reserved for future integrations)
   - Why: Standard library for making HTTP requests in Python

### Additional Libraries
- **google-generativeai (0.3.2)** - Gemini API integration for AI assistant
- **python-dotenv (1.0.1)** - Environment variable management
- **pytest (8.0.0)** - Testing framework

---

## 📋 Prerequisites

- **Windows Operating System**
- **Python 3.8 or higher** installed
- **PowerShell** or Command Prompt access
- (Optional) **Gemini API Key** for AI features

---

## 🚀 Installation

### Step 1: Navigate to Project Directory

Open PowerShell and navigate to the FoodMind AI project:

```powershell
cd "c:\Users\Saurav\Downloads\Foodmind AI .py"
```

### Step 2: Create Virtual Environment

```powershell
python -m venv venv
```

### Step 3: Activate Virtual Environment

```powershell
.\venv\Scripts\Activate.ps1
```

If you encounter execution policy errors, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again.

### Step 4: Install Dependencies

```powershell
pip install -r requirements.txt
```

This installs:
- streamlit
- pillow
- pandas
- matplotlib
- requests
- google-generativeai
- pytest
- python-dotenv

### Step 5: (Optional) Configure Gemini AI

To enable the AI nutrition assistant:

1. Get a free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

2. Create a `.env` file in the project root:

```powershell
copy .env.example .env
```

3. Edit `.env` and add your API key:

```
GEMINI_API_KEY=your_actual_api_key_here
```

**Note:** The app works fully without the API key. Only the AI Assistant feature requires it.

---

## ▶️ Running the Application

### Start the Application

```powershell
streamlit run app.py
```

### Access the Application

The application will automatically open in your default browser at:

```
http://localhost:8501
```

If it doesn't open automatically, copy and paste the URL from the terminal.

### Stop the Application

Press `Ctrl + C` in the PowerShell terminal.

---

## 📁 Project Structure

```
Foodmind AI .py/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .gitignore                  # Git ignore rules
├── .env.example                # Environment variables template
│
├── database/
│   ├── db.py                   # Database manager and operations
│   ├── schema.sql              # Database schema definition
│   └── foodmind.db             # SQLite database (auto-created)
│
├── data/
│   └── food_database.csv       # Food nutrition database (50+ items)
│
├── modules/
│   ├── dashboard.py            # Dashboard page
│   ├── food_analysis.py        # Food search and image analysis
│   ├── meal_tracking.py        # Meal logging and history
│   ├── ai_assistant.py         # AI chat interface
│   ├── profile.py              # User profile and goals
│   └── reports.py              # Nutrition visualizations
│
├── utils/
│   ├── nutrition.py            # BMI, BMR, TDEE calculations
│   ├── validators.py           # Input validation
│   └── image_processing.py     # Image handling with Pillow
│
├── tests/
│   ├── test_nutrition.py       # Nutrition calculation tests
│   └── test_database.py        # Database operation tests
│
├── assets/                     # Static assets (images, etc.)
└── exports/                    # CSV export files (auto-created)
```

---

## 🧪 Testing

### Run All Tests

```powershell
pytest tests/ -v
```

### Run Specific Test File

```powershell
pytest tests/test_nutrition.py -v
```

### Run Tests with Coverage

```powershell
pip install pytest-cov
pytest tests/ --cov=utils --cov=database -v
```

### Test Coverage

The test suite includes:
- **Nutrition Calculations**: BMI, BMR, TDEE, macronutrient targets
- **Database Operations**: CRUD operations, data integrity
- **Validation**: Input sanitization and validation
- **Edge Cases**: Zero values, boundary conditions

---

## 🎯 Usage Guide

### First Time Setup

1. **Launch the application**
2. **Navigate to "Profile & Goals"** in the sidebar
3. **Enter your personal information:**
   - Name, age, height, weight
   - Activity level
   - Dietary preference
   - Nutrition goal
4. **Save your profile** - Goals are automatically calculated
5. **Return to Dashboard** to see your personalized overview

### Daily Usage

1. **Log Meals:**
   - Go to "Meal Tracking"
   - Select meal type (breakfast, lunch, dinner, snack)
   - Choose from food database or enter manually
   - Submit

2. **View Progress:**
   - Dashboard shows today's nutrition
   - Check progress bars for macronutrients
   - View weekly calorie trends

3. **Analyze Foods:**
   - Use "Food Analysis" to search foods
   - Upload images for AI recognition (if configured)
   - Calculate serving adjustments

4. **Get AI Guidance:**
   - Visit "AI Assistant"
   - Ask nutrition questions
   - Get personalized meal suggestions

5. **Review Reports:**
   - Go to "Nutrition Reports"
   - View charts and trends
   - Export data to CSV

---

## 📊 Food Database

The application includes a comprehensive food database with 50+ common foods:

### Categories
- **Grains**: Rice, Chapati, Roti, Bread, Oats, Poha, Idli, Dosa
- **Legumes**: Dal, Moong Dal, Masoor Dal, Rajma, Chickpeas
- **Protein**: Eggs, Chicken, Fish, Paneer
- **Dairy**: Milk, Yogurt
- **Fruits**: Banana, Apple, Orange, Mango, Papaya, Watermelon
- **Vegetables**: Potato, Sweet Potato, Spinach, Broccoli, Tomato, Carrot, Onion
- **Nuts**: Almonds, Cashews, Walnuts, Peanuts
- **Fats & Oils**: Ghee, Butter, Olive Oil, Coconut Oil

### Nutrition Information Per Item
- Serving size (standardized)
- Calories (kcal)
- Protein (g)
- Carbohydrates (g)
- Fat (g)
- Fiber (g)

**Note:** All values are estimates based on USDA and Indian food composition data. Actual values vary based on preparation, ingredients, and brands.

---

## 🔐 Security & Privacy

### Data Storage
- **All data is stored locally** in SQLite database
- **No data is sent to external servers** (except optional AI requests)
- **Database file**: `database/foodmind.db`

### API Key Security
- API keys stored in `.env` (not committed to git)
- `.env` is listed in `.gitignore`
- Never hardcode sensitive credentials

### Best Practices
- Keep your `.env` file private
- Don't share your API key
- Regularly backup your database file

---

## ⚠️ Important Disclaimers

### Medical Disclaimer

**FoodMind AI is an educational nutrition tracking tool.**

- ✅ Use for: General nutrition awareness and food logging
- ❌ Not a substitute for: Professional medical or dietetic advice
- ⚠️ Limitations:
  - Calculations use standard formulas (individual needs vary)
  - Nutrition data is estimated (actual values vary)
  - Does not account for medical conditions or medications
  - Not suitable for diagnosis or treatment

**Consult healthcare professionals for:**
- Personalized nutrition plans
- Medical conditions requiring dietary modifications
- Eating disorders
- Weight management with health complications
- Pregnancy or special health needs

### Nutrition Data Accuracy

- Values are based on reference sources (USDA, IFCT)
- Actual nutrition varies by:
  - Specific brands and products
  - Preparation methods
  - Ingredient quality
  - Portion measurement accuracy

### AI Assistant

- AI responses are informational, not medical advice
- Powered by Google Gemini API
- Requires active internet connection
- Subject to API rate limits and availability

---

## 🐛 Troubleshooting

### Application Won't Start

**Issue:** `streamlit: command not found`

**Solution:** Ensure virtual environment is activated:
```powershell
.\venv\Scripts\Activate.ps1
```

### Database Errors

**Issue:** Database locked or permission errors

**Solution:** 
1. Close all application instances
2. Check file permissions on `database/` folder
3. Delete `foodmind.db` to recreate (loses data)

### Import Errors

**Issue:** `ModuleNotFoundError`

**Solution:** Reinstall dependencies:
```powershell
pip install -r requirements.txt --force-reinstall
```

### AI Assistant Not Working

**Issue:** "API key not configured"

**Solution:**
1. Verify `.env` file exists
2. Check API key is correct
3. Restart application after adding key
4. Test API key at [Google AI Studio](https://makersuite.google.com/)

### Image Upload Fails

**Issue:** Images not processing

**Solution:**
1. Check file size (max 5MB)
2. Use supported formats (JPEG, PNG, WebP)
3. Ensure Pillow is installed: `pip install pillow`

---

## 🔄 Future Enhancements

Potential features for future versions:

- 🔐 Multi-user support with authentication
- 📱 Mobile-responsive design improvements
- 🍳 Recipe nutritional analysis
- 🎯 Goal progress tracking over time
- 📧 Email reports and reminders
- 🔗 Fitness tracker integrations
- 🌍 Multi-language support
- 📚 Expanded food database
- 🏋️ Exercise tracking
- 📸 Improved AI image recognition

---

## 📄 License

This project is created for educational purposes. 

### Third-Party Licenses
- Streamlit - Apache License 2.0
- Pillow - PIL License
- Pandas - BSD 3-Clause
- Matplotlib - PSF-based License
- Google Generative AI - Google Terms of Service

---

## 🤝 Contributing

This is an educational project. For improvements:

1. Test thoroughly on Windows
2. Follow existing code style
3. Update tests for new features
4. Update README for user-facing changes

---

## 📞 Support

### Common Issues
- Check the Troubleshooting section
- Verify all dependencies are installed
- Ensure Python 3.8+ is being used

### Resources
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Pillow Documentation](https://pillow.readthedocs.io/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Gemini API Documentation](https://ai.google.dev/docs)

---

## 🎓 Educational Value

### Learning Outcomes

This project demonstrates:

1. **Web Development**: Building interactive web apps with Streamlit
2. **Database Design**: SQLite schema design and CRUD operations
3. **Data Processing**: Using Pandas for CSV and data manipulation
4. **Visualization**: Creating charts with Matplotlib
5. **Image Processing**: Handling uploads with Pillow
6. **AI Integration**: Using generative AI APIs
7. **Testing**: Unit testing with pytest
8. **Security**: Environment variable management
9. **Project Structure**: Modular Python application design
10. **Documentation**: Comprehensive README and code comments

### Key Concepts Covered

- MVC-like architecture in Python
- Database normalization and relationships
- Input validation and sanitization
- Error handling and user feedback
- State management in web apps
- API integration and error handling
- Image validation and processing
- Mathematical calculations (BMI, BMR, TDEE)
- Data aggregation and reporting
- CSV import/export
- Virtual environments
- Dependency management

---

## ✅ Verification Checklist

After installation, verify:

- [x] Application starts without errors
- [x] Dashboard loads and shows welcome message (new user)
- [x] Can create user profile
- [x] Can search food database
- [x] Can log meals (meals persist after restart)
- [x] Meals appear in meal tracking section
- [x] Can delete meals
- [x] Dashboard shows logged meals and nutrition
- [x] Nutrition reports generate charts
- [x] Charts use actual saved data (not random)
- [x] CSV export works
- [x] Image upload validates file type
- [x] Images are processed and resized
- [x] AI assistant shows setup instructions (without key)
- [x] Tests pass: `pytest tests/ -v`
- [x] All files are inside authorized directory

---

## 🎉 Acknowledgments

Built with:
- Python community
- Streamlit team
- Google Gemini AI
- Open source contributors

Nutrition data sources:
- USDA FoodData Central
- Indian Food Composition Tables (IFCT)

---

## 📊 Project Statistics

- **Total Files**: 20+
- **Lines of Code**: 3000+
- **Python Libraries**: 8
- **Test Cases**: 25+
- **Food Database Items**: 50+
- **Features**: 30+

---

**Built with ❤️ for health and nutrition awareness**

*FoodMind AI - Your journey to better nutrition starts here* 🥗
