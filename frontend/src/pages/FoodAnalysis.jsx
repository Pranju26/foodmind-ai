import { useState } from "react";
import AppShell from "../components/AppShell";
import FoodScanner from "../components/FoodScanner";
import AddMealForm from "../components/AddMealForm";
import { apiUpload } from "../api/client";
import "./FoodAnalysis.css";

function FoodAnalysis() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [showLogForm, setShowLogForm] = useState(false);

  async function handleAnalyze(file) {
    setLoading(true);
    setError("");
    setResult(null);
    setShowLogForm(false);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const data = await apiUpload("/food/analyze", formData);
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <AppShell title="Food Scanner" subtitle="Upload a photo and let FoodMind AI identify what's on your plate.">
      <div className="analysis-layout">
        <FoodScanner onAnalyze={handleAnalyze} loading={loading} />

        <div className="analysis-result-panel">
          {!result && !error && !loading && (
            <div className="analysis-empty">
              <p>Your analysis will appear here.</p>
              <p className="analysis-empty-sub">
                FoodMind AI identifies the food, then checks it against our verified nutrition database.
              </p>
            </div>
          )}

          {loading && (
            <div className="analysis-loading">
              <div className="analysis-skeleton-line" style={{ width: "60%" }}></div>
              <div className="analysis-skeleton-line" style={{ width: "40%" }}></div>
              <div className="analysis-skeleton-block"></div>
            </div>
          )}

          {error && (
            <div className="analysis-error">
              <p>Something went wrong analyzing this image.</p>
              <p className="analysis-error-detail">{error}</p>
            </div>
          )}

          {result && (
            <div className="analysis-result">
              <p className="analysis-result-label">Food detected</p>
              <h2>{result.identified_food}</h2>

              {result.matched_in_database ? (
                <>
                  <p className="analysis-matched-tag">Matched in our nutrition database</p>
                  <div className="analysis-nutrition-grid">
                    <div className="analysis-nutrition-item">
                      <span>Calories (per 100g)</span>
                      <strong>{result.nutrition.calories_per_100g} kcal</strong>
                    </div>
                    <div className="analysis-nutrition-item">
                      <span>Protein (per 100g)</span>
                      <strong>{result.nutrition.protein_per_100g} g</strong>
                    </div>
                    <div className="analysis-nutrition-item">
                      <span>Carbs (per 100g)</span>
                      <strong>{result.nutrition.carbs_per_100g} g</strong>
                    </div>
                    <div className="analysis-nutrition-item">
                      <span>Fat (per 100g)</span>
                      <strong>{result.nutrition.fat_per_100g} g</strong>
                    </div>
                  </div>
                  <p className="analysis-note">{result.note}</p>

                  <button className="analysis-log-btn" onClick={() => setShowLogForm(!showLogForm)}>
                    {showLogForm ? "Cancel" : "Log this to a meal"}
                  </button>

                  {showLogForm && (
                    <AddMealForm
                      prefill={{ food_id: result.food_id }}
                      onLogged={() => setShowLogForm(false)}
                    />
                  )}
                </>
              ) : (
                <div className="analysis-unmatched">
                  <p className="analysis-unmatched-tag">Not yet in our database</p>
                  <p className="analysis-note">{result.note}</p>

                  <button className="analysis-log-btn" onClick={() => setShowLogForm(!showLogForm)}>
                    {showLogForm ? "Cancel" : "Log a food manually instead"}
                  </button>

                  {showLogForm && (
                    <AddMealForm onLogged={() => setShowLogForm(false)} />
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </AppShell>
  );
}

export default FoodAnalysis;
