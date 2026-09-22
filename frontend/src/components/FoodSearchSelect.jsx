import { useState, useEffect, useRef } from "react";
import { apiGet, apiPost } from "../api/client";
import "./FoodSearchSelect.css";

function FoodSearchSelect({ value, onSelect }) {
  const [query, setQuery] = useState(value ? value.name : "");
  const [results, setResults] = useState([]);
  const [searching, setSearching] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [error, setError] = useState("");
  const [open, setOpen] = useState(false);
  const debounceRef = useRef(null);

  useEffect(() => {
    if (!open) return;
    if (query.trim().length < 2) {
      setResults([]);
      return;
    }

    if (debounceRef.current) clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(async () => {
      setSearching(true);
      setError("");
      try {
        const data = await apiGet(`/foods/search?q=${encodeURIComponent(query.trim())}`);
        setResults(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setSearching(false);
      }
    }, 350);

    return () => clearTimeout(debounceRef.current);
  }, [query, open]);

  function handlePick(food) {
    setQuery(food.name);
    setResults([]);
    setOpen(false);
    onSelect(food);
  }

  async function handleAnalyzeNew() {
    setAnalyzing(true);
    setError("");
    try {
      const food = await apiPost("/foods/analyze-name", { name: query.trim() });
      handlePick(food);
    } catch (err) {
      setError(err.message);
    } finally {
      setAnalyzing(false);
    }
  }

  return (
    <div className="food-search-wrapper">
      <input
        type="text"
        className="food-search-input"
        placeholder="Search for a food..."
        value={query}
        onChange={(e) => {
          setQuery(e.target.value);
          setOpen(true);
          onSelect(null);
        }}
        onFocus={() => setOpen(true)}
      />

      {open && query.trim().length >= 2 && (
        <div className="food-search-dropdown">
          {searching && <div className="food-search-status">Searching...</div>}

          {!searching && results.length > 0 && (
            <ul className="food-search-results">
              {results.map((food) => (
                <li key={food.id} onClick={() => handlePick(food)}>
                  <span>{food.name}</span>
                  {!food.is_verified && <span className="food-search-ai-tag">AI estimated</span>}
                </li>
              ))}
            </ul>
          )}

          {!searching && results.length === 0 && (
            <div className="food-search-empty">
              <p>No match found for "{query}".</p>
              <button type="button" onClick={handleAnalyzeNew} disabled={analyzing}>
                {analyzing ? "FoodMind AI is analyzing..." : `+ Analyze "${query}" with FoodMind AI`}
              </button>
            </div>
          )}

          {error && <div className="food-search-error">{error}</div>}
        </div>
      )}
    </div>
  );
}

export default FoodSearchSelect;
