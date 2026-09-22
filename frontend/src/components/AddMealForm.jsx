import { useState, useEffect } from "react";
import { apiGet, apiPost } from "../api/client";
import FoodSearchSelect from "./FoodSearchSelect";
import "./AddMealForm.css";

function AddMealForm({ prefill, onLogged }) {
  const [mealType, setMealType] = useState("breakfast");
  const [items, setItems] = useState([{ food: null, grams: "" }]);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadPrefill() {
      if (prefill && prefill.food_id) {
        try {
          const results = await apiGet(`/foods/search?q=`);
        } catch (err) {
          // ignore, prefill is best-effort
        }
      }
    }
    if (prefill && prefill.food_id && prefill.food_name) {
      setItems([{
        food: {
          id: prefill.food_id,
          name: prefill.food_name,
          is_verified: prefill.is_verified !== false,
        },
        grams: "100",
      }]);
    }
  }, [prefill]);

  function updateItemFood(index, food) {
    const next = [...items];
    next[index].food = food;
    setItems(next);
  }

  function updateItemGrams(index, grams) {
    const next = [...items];
    next[index].grams = grams;
    setItems(next);
  }

  function addItemRow() {
    setItems([...items, { food: null, grams: "" }]);
  }

  function removeItemRow(index) {
    setItems(items.filter((_, i) => i !== index));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setSaving(true);
    setMessage("");
    setError("");

    try {
      const payload = {
        meal_type: mealType,
        items: items
          .filter((i) => i.food && i.grams)
          .map((i) => ({ food_id: i.food.id, grams: Number(i.grams) })),
      };

      if (payload.items.length === 0) {
        throw new Error("Search and select at least one food with a gram amount.");
      }

      await apiPost("/meals", payload);
      setMessage("Meal logged successfully.");
      setItems([{ food: null, grams: "" }]);
      if (onLogged) onLogged();
    } catch (err) {
      setError(err.message);
    } finally {
      setSaving(false);
    }
  }

  return (
    <form className="add-meal-form" onSubmit={handleSubmit}>
      <div className="add-meal-row">
        <label>Meal type</label>
        <select value={mealType} onChange={(e) => setMealType(e.target.value)}>
          <option value="breakfast">Breakfast</option>
          <option value="lunch">Lunch</option>
          <option value="dinner">Dinner</option>
          <option value="snack">Snack</option>
        </select>
      </div>

      {items.map((item, idx) => (
        <div key={idx} className="add-meal-item-row">
          <FoodSearchSelect value={item.food} onSelect={(food) => updateItemFood(idx, food)} />
          <input
            type="number"
            placeholder="grams"
            value={item.grams}
            onChange={(e) => updateItemGrams(idx, e.target.value)}
            required
          />
          {items.length > 1 && (
            <button type="button" className="add-meal-remove" onClick={() => removeItemRow(idx)}>
              ×
            </button>
          )}
        </div>
      ))}

      <button type="button" className="add-meal-add-row" onClick={addItemRow}>
        + Add another food
      </button>

      {message && <p className="add-meal-message">{message}</p>}
      {error && <p className="add-meal-error">{error}</p>}

      <button type="submit" className="add-meal-submit" disabled={saving}>
        {saving ? "Logging..." : "Log meal"}
      </button>
    </form>
  );
}

export default AddMealForm;
