import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { apiPost } from "../api/client";
import "./AuthPages.css";

function Register() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);

  const navigate = useNavigate();

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      await apiPost("/auth/register", { email, password });
      setSuccess(true);
      setTimeout(() => navigate("/login"), 1500);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="auth-page">
      <div className="auth-brand-panel">
        <h1>🥗 FoodMind AI</h1>
        <p>Your intelligent food and nutrition assistant.</p>
      </div>

      <div className="auth-form-panel">
        <div className="auth-form-box">
          <h2>Create your account</h2>
          <p className="auth-subtitle">Start tracking meals in a minute.</p>

          {success ? (
            <p style={{ color: "#1B3B2F" }}>Account created. Redirecting to login...</p>
          ) : (
            <form onSubmit={handleSubmit}>
              <label htmlFor="email">Email</label>
              <input
                id="email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />

              <label htmlFor="password">Password</label>
              <input
                id="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />

              {error && <p className="auth-error">{error}</p>}

              <button type="submit" disabled={loading}>
                {loading ? "Creating account..." : "Create account"}
              </button>
            </form>
          )}

          <p className="auth-switch">
            Already have an account? <Link to="/login">Log in</Link>
          </p>
        </div>
      </div>
    </div>
  );
}

export default Register;
