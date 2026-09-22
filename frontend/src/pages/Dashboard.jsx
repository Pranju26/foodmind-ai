import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import AppShell from "../components/AppShell";
import { apiGet } from "../api/client";
import "./Dashboard.css";

function Dashboard() {
  const [targets, setTargets] = useState(null);
  const [meals, setMeals] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    async function loadData() {
      try {
        const targetsData = await apiGet("/nutrition/targets");
        setTargets(targetsData);
      } catch (err) {
        setError(err.message);
      }

      try {
        const mealsData = await apiGet("/meals");
        setMeals(mealsData);
      } catch (err) {
        console.error(err.message);
      }

      setLoading(false);
    }

    loadData();
  }, []);

  const todaysMeals = meals.filter((meal) => {
    const mealDate = new Date(meal.logged_at).toDateString();
    const today = new Date().toDateString();
    return mealDate === today;
  });

  const hasEarlierMeals = meals.length > todaysMeals.length;

  const totalCalories = todaysMeals.reduce((sum, m) => sum + m.total_calories, 0);
  const totalProtein = todaysMeals.reduce((sum, m) => sum + m.total_protein, 0);
  const totalCarbs = todaysMeals.reduce((sum, m) => sum + m.total_carbs, 0);
  const totalFat = todaysMeals.reduce((sum, m) => sum + m.total_fat, 0);

  let nutritionScore = null;
  let scoreInsight = "";

  if (targets) {
    const pctOfTarget = totalCalories / targets.calorie_target;
    nutritionScore = Math.round(Math.min(pctOfTarget, 1.15) * 100 > 100
      ? 200 - Math.min(pctOfTarget, 1.15) * 100
      : pctOfTarget * 100);
    nutritionScore = Math.max(0, Math.min(100, nutritionScore));

    const proteinPct = (totalProtein / targets.protein_grams) * 100;
    if (totalCalories === 0) {
      scoreInsight = "You haven't logged any meals yet today.";
    } else if (proteinPct < 70) {
      scoreInsight = `Your protein intake is at ${proteinPct.toFixed(0)}% of today's target. Consider adding a protein-rich food.`;
    } else if (pctOfTarget > 1.1) {
      scoreInsight = "You've gone over your calorie target for today.";
    } else {
      scoreInsight = "You're tracking well against today's targets.";
    }
  }

  const circumference = 2 * Math.PI * 54;
  const scoreOffset = nutritionScore !== null ? circumference - (nutritionScore / 100) * circumference : circumference;

  return (
    <AppShell title="Good to see you 👋" subtitle="Here's your nutrition snapshot for today.">
      {loading ? (
        <p className="preview-loading">Loading your dashboard...</p>
      ) : (
        <>
          <div className="dashboard-quick-actions">
            <button onClick={() => navigate("/food-analysis")}>Scan a meal</button>
            <button onClick={() => navigate("/meals")}>Log a meal</button>
            <button onClick={() => navigate("/ai-assistant")}>Ask FoodMind AI</button>
          </div>

          {error && (
            <div className="preview-card preview-warning">
              <p>{error}</p>
              <p className="preview-hint">Set up your profile to see personalized targets.</p>
            </div>
          )}

          {targets && (
            <div className="preview-hero">
              <div className="preview-score-ring">
                <svg width="140" height="140" viewBox="0 0 120 120">
                  <circle cx="60" cy="60" r="54" fill="none" stroke="#E8ECE2" strokeWidth="10" />
                  <circle
                    cx="60"
                    cy="60"
                    r="54"
                    fill="none"
                    stroke="var(--color-accent)"
                    strokeWidth="10"
                    strokeDasharray={circumference}
                    strokeDashoffset={scoreOffset}
                    strokeLinecap="round"
                    transform="rotate(-90 60 60)"
                  />
                </svg>
                <div className="preview-score-label">
                  <span className="preview-score-number">{nutritionScore}</span>
                  <span className="preview-score-max">/ 100</span>
                </div>
              </div>

              <div className="preview-hero-text">
                <h2>Your nutrition, understood.</h2>
                <p className="preview-insight-box">
                  🤖 <strong>AI Insight:</strong> {scoreInsight}
                </p>
              </div>
            </div>
          )}

          {targets && (
            <div className="preview-macros">
              <MacroBar label="Calories" value={totalCalories} target={targets.calorie_target} unit="kcal" />
              <MacroBar label="Protein" value={totalProtein} target={targets.protein_grams} unit="g" />
              <MacroBar label="Carbs" value={totalCarbs} target={targets.carb_grams} unit="g" />
              <MacroBar label="Fat" value={totalFat} target={targets.fat_grams} unit="g" />
            </div>
          )}

          <div className="preview-section-header">
            <h3 className="preview-section-title">Today's meals</h3>
            {hasEarlierMeals && (
              <button className="dashboard-link-btn" onClick={() => navigate("/meals")}>
                View full history →
              </button>
            )}
          </div>

          {todaysMeals.length === 0 ? (
            <div className="preview-empty">
              <p className="preview-empty-title">Your nutrition journey starts with your first meal.</p>
              <button className="preview-empty-btn" onClick={() => navigate("/food-analysis")}>
                Analyze your first meal
              </button>
            </div>
          ) : (
            <div className="preview-timeline">
              {todaysMeals.map((meal) => (
                <div key={meal.id} className="preview-timeline-item">
                  <div className="preview-timeline-time">
                    {new Date(meal.logged_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                  </div>
                  <div className="preview-timeline-content">
                    <strong>{meal.meal_type}</strong>
                    <span className="preview-timeline-foods">
                      {meal.items.map((i) => i.food_name).join(", ")}
                    </span>
                    <span className="preview-timeline-cal">{meal.total_calories} kcal</span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </>
      )}
    </AppShell>
  );
}

function MacroBar({ label, value, target, unit }) {
  const pct = target ? Math.min((value / target) * 100, 100) : 0;
  return (
    <div className="macro-bar">
      <div className="macro-bar-labels">
        <span>{label}</span>
        <span>{value.toFixed(0)} / {target} {unit}</span>
      </div>
      <div className="macro-bar-track">
        <div className="macro-bar-fill" style={{ width: `${pct}%` }}></div>
      </div>
    </div>
  );
}

export default Dashboard;
