import os
from datetime import datetime, timedelta, timezone
from typing import Optional, List

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext
from jose import jwt, JWTError
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from app.database.connection import get_db, engine, Base
from app.models.user import User
from app.models.profile import Profile
from app.models.food import Food
from app.models.meal import Meal, MealItem
from app.services.nutrition_engine import calculate_full_nutrition_targets

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI()

import logging
logger = logging.getLogger("foodmind")
logging.basicConfig(level=logging.INFO)

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "YOUR_VERCEL_URL"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRE_MINUTES = int(os.getenv("JWT_EXPIRE_MINUTES", "60"))


def create_access_token(email: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_EXPIRE_MINUTES)
    payload = {"sub": email, "exp": expire}
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)


@app.get("/")
def read_root():
    return {"message": "FoodMind AI backend is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


# ---------------- FOOD LOOKUP ----------------

FAKE_FOOD_DB = {
    "banana": {"calories": 105, "protein": 1.3, "carbs": 27, "fat": 0.4},
    "rice": {"calories": 130, "protein": 2.7, "carbs": 28, "fat": 0.3},
    "roti": {"calories": 120, "protein": 3.0, "carbs": 18, "fat": 3.7},
}


class FoodQuery(BaseModel):
    food_name: str
    grams: float


@app.post("/food/lookup")
def lookup_food(query: FoodQuery):
    food_name = query.food_name.lower()
    if food_name not in FAKE_FOOD_DB:
        raise HTTPException(status_code=404, detail="Food not found in database")
    food = FAKE_FOOD_DB[food_name]
    scale = query.grams / 100
    return {
        "food_name": query.food_name,
        "grams": query.grams,
        "calories": round(food["calories"] * scale, 1),
        "protein": round(food["protein"] * scale, 1),
        "carbs": round(food["carbs"] * scale, 1),
        "fat": round(food["fat"] * scale, 1),
    }


# ---------------- AUTH: REGISTER ----------------

class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)


class UserPublic(BaseModel):
    email: EmailStr


@app.post("/auth/register", response_model=UserPublic)
def register_user(user: UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(user.password)

    new_user = User(email=user.email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"email": new_user.email}


# ---------------- AUTH: LOGIN ----------------

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@app.post("/auth/login", response_model=TokenResponse)
@limiter.limit("5/minute")
def login_user(request: Request, credentials: UserLogin, db: Session = Depends(get_db)):
    stored_user = db.query(User).filter(User.email == credentials.email).first()

    if not stored_user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    password_matches = pwd_context.verify(credentials.password, stored_user.password_hash)

    if not password_matches:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    token = create_access_token(credentials.email)

    return {"access_token": token, "token_type": "bearer"}


# ---------------- PROTECTED ROUTE: GET CURRENT USER ----------------

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> str:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception

    return email


@app.get("/users/me", response_model=UserPublic)
def read_current_user(current_user_email: str = Depends(get_current_user)):
    return {"email": current_user_email}


# ---------------- PROFILE ----------------

class ProfileInput(BaseModel):
    sex: Optional[str] = None
    age: Optional[int] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    activity_level: Optional[str] = None
    dietary_preference: Optional[str] = None
    goal: Optional[str] = None


class ProfileOutput(BaseModel):
    sex: Optional[str] = None
    age: Optional[int] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    activity_level: Optional[str] = None
    dietary_preference: Optional[str] = None
    goal: Optional[str] = None

    class Config:
        from_attributes = True


@app.post("/profile", response_model=ProfileOutput)
def create_or_update_profile(
    profile_data: ProfileInput,
    current_user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == current_user_email).first()

    existing_profile = db.query(Profile).filter(Profile.user_id == user.id).first()

    if existing_profile:
        existing_profile.sex = profile_data.sex
        existing_profile.age = profile_data.age
        existing_profile.height_cm = profile_data.height_cm
        existing_profile.weight_kg = profile_data.weight_kg
        existing_profile.activity_level = profile_data.activity_level
        existing_profile.dietary_preference = profile_data.dietary_preference
        existing_profile.goal = profile_data.goal
        db.commit()
        db.refresh(existing_profile)
        return existing_profile

    new_profile = Profile(
        user_id=user.id,
        sex=profile_data.sex,
        age=profile_data.age,
        height_cm=profile_data.height_cm,
        weight_kg=profile_data.weight_kg,
        activity_level=profile_data.activity_level,
        dietary_preference=profile_data.dietary_preference,
        goal=profile_data.goal,
    )
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return new_profile


@app.get("/profile", response_model=ProfileOutput)
def get_profile(
    current_user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == current_user_email).first()
    profile = db.query(Profile).filter(Profile.user_id == user.id).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found. Please create one first.")

    return profile


# ---------------- MEALS ----------------

class MealItemInput(BaseModel):
    food_id: int
    grams: float


class MealCreate(BaseModel):
    meal_type: str
    items: List[MealItemInput]


class MealItemOutput(BaseModel):
    food_id: int
    food_name: str
    grams: float
    calories: float
    protein: float
    carbs: float
    fat: float


class MealOutput(BaseModel):
    id: int
    meal_type: str
    logged_at: datetime
    items: List[MealItemOutput]
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fat: float


def build_meal_output(meal: Meal) -> dict:
    items_output = []
    total_calories = 0.0
    total_protein = 0.0
    total_carbs = 0.0
    total_fat = 0.0

    for item in meal.items:
        scale = item.grams / 100
        calories = round(item.food.calories_per_100g * scale, 1)
        protein = round(item.food.protein_per_100g * scale, 1)
        carbs = round(item.food.carbs_per_100g * scale, 1)
        fat = round(item.food.fat_per_100g * scale, 1)

        items_output.append({
            "food_id": item.food_id,
            "food_name": item.food.name,
            "grams": item.grams,
            "calories": calories,
            "protein": protein,
            "carbs": carbs,
            "fat": fat,
        })

        total_calories += calories
        total_protein += protein
        total_carbs += carbs
        total_fat += fat

    return {
        "id": meal.id,
        "meal_type": meal.meal_type,
        "logged_at": meal.logged_at,
        "items": items_output,
        "total_calories": round(total_calories, 1),
        "total_protein": round(total_protein, 1),
        "total_carbs": round(total_carbs, 1),
        "total_fat": round(total_fat, 1),
    }


@app.post("/meals", response_model=MealOutput)
def create_meal(
    meal_data: MealCreate,
    current_user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == current_user_email).first()

    new_meal = Meal(user_id=user.id, meal_type=meal_data.meal_type)
    db.add(new_meal)
    db.commit()
    db.refresh(new_meal)

    for item in meal_data.items:
        food = db.query(Food).filter(Food.id == item.food_id).first()
        if not food:
            raise HTTPException(status_code=404, detail=f"Food with id {item.food_id} not found")

        meal_item = MealItem(meal_id=new_meal.id, food_id=item.food_id, grams=item.grams)
        db.add(meal_item)

    db.commit()
    db.refresh(new_meal)

    return build_meal_output(new_meal)


@app.get("/meals", response_model=List[MealOutput])
def get_meals(
    current_user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == current_user_email).first()
    meals = db.query(Meal).filter(Meal.user_id == user.id).order_by(Meal.logged_at.desc()).all()

    return [build_meal_output(meal) for meal in meals]


# ---------------- NUTRITION TARGETS ----------------

class NutritionTargets(BaseModel):
    bmr: float
    tdee: float
    calorie_target: float
    protein_grams: float
    fat_grams: float
    carb_grams: float
    disclaimer: str = "These are estimates based on standard formulas, not personalized medical advice. Consult a professional for medical guidance."


@app.get("/nutrition/targets", response_model=NutritionTargets)
def get_nutrition_targets(
    current_user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == current_user_email).first()
    profile = db.query(Profile).filter(Profile.user_id == user.id).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found. Please create one first.")

    required_fields = [profile.sex, profile.weight_kg, profile.height_cm, profile.age, profile.activity_level, profile.goal]
    if any(field is None for field in required_fields):
        raise HTTPException(
            status_code=400,
            detail="Incomplete profile. Please provide sex, weight, height, age, activity_level, and goal.",
        )

    targets = calculate_full_nutrition_targets(
        sex=profile.sex,
        weight_kg=profile.weight_kg,
        height_cm=profile.height_cm,
        age=profile.age,
        activity_level=profile.activity_level,
        goal=profile.goal,
    )

    return targets


# ---------------- AI CHAT ----------------

from google import genai

gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    reply: str


@app.post("/ai/chat", response_model=ChatResponse)
@limiter.limit("10/minute")
def ai_chat(
    request: Request,
    chat_request: ChatRequest,
    current_user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == current_user_email).first()
    profile = db.query(Profile).filter(Profile.user_id == user.id).first()

    context_lines = ["You are a helpful, friendly nutrition assistant for an app called FoodMind AI."]

    if profile and profile.goal:
        context_lines.append(f"The user's fitness goal is: {profile.goal}.")
    if profile and profile.dietary_preference:
        context_lines.append(f"The user's dietary preference is: {profile.dietary_preference}.")

    context_lines.append(f"User question: {chat_request.message}")
    context_lines.append("Give a concise, practical, encouraging answer in 2-4 sentences.")

    full_prompt = "\n".join(context_lines)

    try:
        response = gemini_client.models.generate_content(
            model="gemini-3.6-flash",
            contents=full_prompt,
        )
        reply_text = response.text
    except Exception as e:
        logger.error(f"AI service error: {e}")
        raise HTTPException(status_code=502, detail="The AI service is temporarily unavailable. Please try again shortly.")

    return {"reply": reply_text}


# ---------------- FOOD IMAGE ANALYSIS ----------------

from fastapi import UploadFile, File
from google.genai import types


class FoodAnalysisResult(BaseModel):
    identified_food: str
    matched_in_database: bool
    food_id: Optional[int] = None
    nutrition: Optional[dict] = None
    note: str


MAX_UPLOAD_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp", "image/heic", "image/heif"}


@app.post("/food/analyze", response_model=FoodAnalysisResult)
@limiter.limit("10/minute")
async def analyze_food_image(
    request: Request,
    file: UploadFile = File(...),
    current_user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Please upload a valid image file (JPEG, PNG, WEBP, or HEIC).")

    image_bytes = await file.read()

    if len(image_bytes) > MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=400, detail="Image is too large. Please upload a file under 5MB.")

    if len(image_bytes) == 0:
        raise HTTPException(status_code=400, detail="The uploaded file is empty.")

    try:
        response = gemini_client.models.generate_content(
            model="gemini-3.6-flash",
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type=file.content_type),
                "Identify the single main food item in this image. "
                "Reply with ONLY the food name, 1-3 words, nothing else. "
                "For example: 'Banana' or 'Grilled Chicken' or 'Fried Rice'."
            ],
        )
        identified_food = response.text.strip()
        if not identified_food or identified_food.lower() in ("none", "null", "n/a", "unknown"):
            raise HTTPException(status_code=422, detail="Could not clearly identify a food in this image. Please try a clearer photo.")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"AI service error: {e}")
        raise HTTPException(status_code=502, detail="The AI service is temporarily unavailable. Please try again shortly.")

    # Try to find a close match in our real food database (case-insensitive, partial match)
    matched_food = (
        db.query(Food)
        .filter(Food.name.ilike(f"%{identified_food}%"))
        .first()
    )

    if not matched_food:
        # Try matching the other way too (in case AI is more general than our DB entry)
        all_foods = db.query(Food).all()
        for food in all_foods:
            if food.name.lower() in identified_food.lower() or identified_food.lower() in food.name.lower():
                matched_food = food
                break

    if matched_food:
        return {
            "identified_food": identified_food,
            "matched_in_database": True,
            "food_id": matched_food.id,
            "nutrition": {
                "calories_per_100g": matched_food.calories_per_100g,
                "protein_per_100g": matched_food.protein_per_100g,
                "carbs_per_100g": matched_food.carbs_per_100g,
                "fat_per_100g": matched_food.fat_per_100g,
            },
            "note": "Nutrition values are per 100g, from our verified food database. Actual serving size may vary.",
        }
    else:
        return {
            "identified_food": identified_food,
            "matched_in_database": False,
            "nutrition": None,
            "note": f"We identified this as '{identified_food}' but don't have verified nutrition data for it yet in our database.",
        }


# ---------------- FOOD CATALOG (read-only list) ----------------

class FoodListItem(BaseModel):
    id: int
    name: str
    calories_per_100g: float
    protein_per_100g: float
    carbs_per_100g: float
    fat_per_100g: float

    class Config:
        from_attributes = True


@app.get("/foods", response_model=List[FoodListItem])
def list_foods(
    current_user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.query(Food).order_by(Food.name).all()


# ---------------- DYNAMIC FOOD SEARCH & AI LOOKUP ----------------

class FoodSearchResult(BaseModel):
    id: int
    name: str
    calories_per_100g: float
    protein_per_100g: float
    carbs_per_100g: float
    fat_per_100g: float
    is_verified: bool

    class Config:
        from_attributes = True


@app.get("/foods/search", response_model=List[FoodSearchResult])
def search_foods(
    q: str,
    current_user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not q or len(q.strip()) < 2:
        return []
    return db.query(Food).filter(Food.name.ilike(f"%{q.strip()}%")).order_by(Food.name).all()


class FoodNameInput(BaseModel):
    name: str


def validate_nutrition_json(data: dict) -> bool:
    required_keys = ["name", "calories_per_100g", "protein_per_100g", "carbs_per_100g", "fat_per_100g"]
    for key in required_keys:
        if key not in data:
            return False
    if not isinstance(data["name"], str) or not data["name"].strip():
        return False
    for key in required_keys[1:]:
        value = data[key]
        if not isinstance(value, (int, float)):
            return False
        if value < 0:
            return False
    return True


@app.post("/foods/analyze-name", response_model=FoodSearchResult)
def analyze_food_name(
    payload: FoodNameInput,
    current_user_email: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    normalized_name = payload.name.strip()

    existing = db.query(Food).filter(Food.name.ilike(normalized_name)).first()
    if existing:
        return existing

    prompt = (
        f"Provide estimated nutrition facts for the food '{normalized_name}', "
        "based on a typical serving/recipe. "
        "Reply with ONLY valid JSON, no other text, no markdown formatting, "
        "in exactly this shape: "
        '{"name": "string", "calories_per_100g": number, "protein_per_100g": number, '
        '"carbs_per_100g": number, "fat_per_100g": number}. '
        "All numeric values must be per 100 grams and non-negative."
    )

    try:
        response = gemini_client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt,
        )
        raw_text = response.text.strip()
        raw_text = raw_text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()

        import json
        parsed = json.loads(raw_text)
    except Exception as e:
        logger.error(f"AI nutrition lookup failed: {e}")
        raise HTTPException(status_code=502, detail="Could not analyze this food right now. Please try again shortly.")

    if not validate_nutrition_json(parsed):
        raise HTTPException(status_code=502, detail="AI returned an invalid or incomplete nutrition response")

    new_food = Food(
        name=parsed["name"].strip(),
        calories_per_100g=float(parsed["calories_per_100g"]),
        protein_per_100g=float(parsed["protein_per_100g"]),
        carbs_per_100g=float(parsed["carbs_per_100g"]),
        fat_per_100g=float(parsed["fat_per_100g"]),
        is_verified=False,
    )
    db.add(new_food)
    db.commit()
    db.refresh(new_food)

    return new_food
