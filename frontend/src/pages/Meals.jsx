import { useState, useEffect } from "react";
import AppShell from "../components/AppShell";
import AddMealForm from "../components/AddMealForm";
import { apiGet } from "../api/client";
import "./Meals.css";

function Meals() {
  const [meals, setMeals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showForm, setShowForm] = useState(false);

  async function loadMeals() {
    try {
      const data = await apiGet("/meals");
      setMeals(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadMeals();
  }, []);

  function handleLogged() {
    setShowForm(false);
    setLoading(true);
    loadMeals();
  }

  const grouped = {};
  meals.forEach((meal) => {
    const dateKey = new Date(meal.logged_at).toDateString();
    if (!grouped[dateKey]) grouped[dateKey] = [];
    grouped[dateKey].push(meal);
  });
  const sortedDates = Object.keys(grouped).sort((a, b) => new Date(b) - new Date(a));

  const last7Days = [];
  for (let i = 6; i >= 0; i--) {
    const d = new Date();
    d.setDate(d.getDate() - i);
    const dateKey = d.toDateString();
    const dayMeals = grouped[dateKey] || [];
    const totalCal = dayMeals.reduce((sum, m) => sum + m.total_calories, 0);
    last7Days.push({
      label: d.toLocaleDateString([], { weekday: "short" }),
      calories: totalCal,
    });
  }
  const maxCal = Math.max(...last7Days.map((d) => d.calories), 1);

  return (
    <AppShell title="Meal history" subtitle="Every meal you've logged, in one place.">
      <div className="meals-header-row">
        <button className="meals-add-btn" onClick={() => setShowForm(!showForm)}>
          {showForm ? "Cancel" : "+ Log a meal"}
        </button>
      </div>

      {showForm && <AddMealForm onLogged={handleLogged} />}

      {loading && <p className="meals-loading">Loading your meal history...</p>}

      {error && <p className="meals-error">{error}</p>}

      {!loading && !error && (
        <>
          <div className="meals-chart-card">
            <h3>Last 7 days</h3>
            <div className="meals-chart">
              {last7Days.map((day, idx) => (
                <div key={idx} className="meals-chart-col">
                  <div className="meals-chart-bar-track">
                    <div
                      className="meals-chart-bar"
                      style={{ height: `${(day.calories / maxCal) * 100}%` }}
                    ></div>
                  </div>
                  <span className="meals-chart-label">{day.label}</span>
                  <span className="meals-chart-value">{day.calories > 0 ? Math.round(day.calories) : "-"}</span>
                </div>
              ))}
            </div>
          </div>

          {sortedDates.length === 0 ? (
            <div className="meals-empty">
              <p>Your nutrition journey starts with your first meal.</p>
            </div>
          ) : (
            sortedDates.map((dateKey) => (
              <div key={dateKey} className="meals-day-group">
                <h3 className="meals-day-title">
                  {new Date(dateKey).toLocaleDateString([], { weekday: "long", month: "short", day: "numeric" })}
                </h3>
                <div className="meals-day-list">
                  {grouped[dateKey].map((meal) => (
                    <div key={meal.id} className="meals-item">
                      <div className="meals-item-time">
                        {new Date(meal.logged_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
                      </div>
                      <div className="meals-item-content">
                        <strong>{meal.meal_type}</strong>
                        <span className="meals-item-foods">
                          {meal.items.map((i) => `${i.food_name} (${i.grams}g)`).join(", ")}
                        </span>
                      </div>
                      <div className="meals-item-cal">{meal.total_calories} kcal</div>
                    </div>
                  ))}
                </div>
              </div>
            ))
          )}
        </>
      )}
    </AppShell>
  );
}

export default Meals;
