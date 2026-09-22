import { useState, useEffect } from "react";
import AppShell from "../components/AppShell";
import { apiGet, apiPost } from "../api/client";
import "./Profile.css";

function Profile() {
  const [form, setForm] = useState({
    sex: "",
    age: "",
    height_cm: "",
    weight_kg: "",
    activity_level: "",
    dietary_preference: "",
    goal: "",
  });
  const [targets, setTargets] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadProfile() {
      try {
        const data = await apiGet("/profile");
        setForm({
          sex: data.sex || "",
          age: data.age || "",
          height_cm: data.height_cm || "",
          weight_kg: data.weight_kg || "",
          activity_level: data.activity_level || "",
          dietary_preference: data.dietary_preference || "",
          goal: data.goal || "",
        });
      } catch (err) {
        // no profile yet - form stays empty
      }

      try {
        const targetsData = await apiGet("/nutrition/targets");
        setTargets(targetsData);
      } catch (err) {
        // targets unavailable until profile is complete
      }

      setLoading(false);
    }
    loadProfile();
  }, []);

  function handleChange(field, value) {
    setForm({ ...form, [field]: value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setSaving(true);
    setMessage("");
    setError("");

    try {
      await apiPost("/profile", {
        sex: form.sex,
        age: Number(form.age),
        height_cm: Number(form.height_cm),
        weight_kg: Number(form.weight_kg),
        activity_level: form.activity_level,
        dietary_preference: form.dietary_preference,
        goal: form.goal,
      });
      setMessage("Profile saved. Your nutrition targets have been updated.");

      try {
        const targetsData = await apiGet("/nutrition/targets");
        setTargets(targetsData);
      } catch (err) {
        // ignore
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  }

  if (loading) {
    return (
      <AppShell title="Profile" subtitle="Your personal details power your nutrition targets.">
        <p className="profile-loading">Loading your profile...</p>
      </AppShell>
    );
  }

  return (
    <AppShell title="Profile" subtitle="Your personal details power your nutrition targets.">
      <div className="profile-layout">
        <form className="profile-form" onSubmit={handleSubmit}>
          <div className="profile-row">
            <div className="profile-field">
              <label>Sex</label>
              <select value={form.sex} onChange={(e) => handleChange("sex", e.target.value)} required>
                <option value="">Select</option>
                <option value="male">Male</option>
                <option value="female">Female</option>
              </select>
            </div>

            <div className="profile-field">
              <label>Age</label>
              <input
                type="number"
                value={form.age}
                onChange={(e) => handleChange("age", e.target.value)}
                required
              />
            </div>
          </div>

          <div className="profile-row">
            <div className="profile-field">
              <label>Height (cm)</label>
              <input
                type="number"
                value={form.height_cm}
                onChange={(e) => handleChange("height_cm", e.target.value)}
                required
              />
            </div>

            <div className="profile-field">
              <label>Weight (kg)</label>
              <input
                type="number"
                value={form.weight_kg}
                onChange={(e) => handleChange("weight_kg", e.target.value)}
                required
              />
            </div>
          </div>

          <div className="profile-row">
            <div className="profile-field">
              <label>Activity level</label>
              <select
                value={form.activity_level}
                onChange={(e) => handleChange("activity_level", e.target.value)}
                required
              >
                <option value="">Select</option>
                <option value="sedentary">Sedentary (little to no exercise)</option>
                <option value="light">Light (1-3 days/week)</option>
                <option value="moderate">Moderate (3-5 days/week)</option>
                <option value="active">Active (6-7 days/week)</option>
                <option value="very_active">Very active (hard exercise + physical job)</option>
              </select>
            </div>

            <div className="profile-field">
              <label>Dietary preference</label>
              <select
                value={form.dietary_preference}
                onChange={(e) => handleChange("dietary_preference", e.target.value)}
                required
              >
                <option value="">Select</option>
                <option value="vegetarian">Vegetarian</option>
                <option value="non_vegetarian">Non-vegetarian</option>
                <option value="vegan">Vegan</option>
              </select>
            </div>
          </div>

          <div className="profile-field">
            <label>Goal</label>
            <select value={form.goal} onChange={(e) => handleChange("goal", e.target.value)} required>
              <option value="">Select</option>
              <option value="weight_loss">Weight loss</option>
              <option value="weight_gain">Weight gain</option>
              <option value="maintain">Maintain weight</option>
              <option value="muscle_gain">Muscle building</option>
            </select>
          </div>

          {message && <p className="profile-message">{message}</p>}
          {error && <p className="profile-error">{error}</p>}

          <button type="submit" disabled={saving}>
            {saving ? "Saving..." : "Save profile"}
          </button>
        </form>

        <aside className="profile-summary">
          <h3>Your nutrition targets</h3>
          {targets ? (
            <div className="profile-summary-list">
              <div className="profile-summary-item">
                <span>Calories</span>
                <strong>{targets.calorie_target} kcal</strong>
              </div>
              <div className="profile-summary-item">
                <span>Protein</span>
                <strong>{targets.protein_grams} g</strong>
              </div>
              <div className="profile-summary-item">
                <span>Carbs</span>
                <strong>{targets.carb_grams} g</strong>
              </div>
              <div className="profile-summary-item">
                <span>Fat</span>
                <strong>{targets.fat_grams} g</strong>
              </div>
              <div className="profile-summary-item">
                <span>BMR</span>
                <strong>{targets.bmr}</strong>
              </div>
              <div className="profile-summary-item">
                <span>TDEE</span>
                <strong>{targets.tdee}</strong>
              </div>
              <p className="profile-disclaimer">{targets.disclaimer}</p>
            </div>
          ) : (
            <p className="profile-summary-empty">
              Complete and save your profile to see your personalized targets here.
            </p>
          )}
        </aside>
      </div>
    </AppShell>
  );
}

export default Profile;
