import { useState, useEffect } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { clearToken } from "../api/client";
import "./Sidebar.css";

const NAV_ITEMS = [
  { to: "/dashboard", label: "Overview", icon: "🏠" },
  { to: "/food-analysis", label: "Food Scanner", icon: "📸" },
  { to: "/meals", label: "Meal History", icon: "🍽️" },
  { to: "/ai-assistant", label: "AI Assistant", icon: "🧠" },
  { to: "/profile", label: "Profile", icon: "👤" },
];

function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);
  const [darkMode, setDarkMode] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const saved = localStorage.getItem("theme");
    const isDark = saved === "dark";
    setDarkMode(isDark);
    document.body.classList.toggle("dark", isDark);
  }, []);

  function toggleDarkMode() {
    const next = !darkMode;
    setDarkMode(next);
    document.body.classList.toggle("dark", next);
    localStorage.setItem("theme", next ? "dark" : "light");
  }

  function handleLogout() {
    clearToken();
    navigate("/login");
  }

  return (
    <aside className={`sidebar ${collapsed ? "sidebar-collapsed" : ""}`}>
      <div className="sidebar-top">
        <div className="sidebar-logo">
          <span>🥗</span>
          {!collapsed && <span className="sidebar-logo-text">FoodMind AI</span>}
        </div>
        <button className="sidebar-toggle" onClick={() => setCollapsed(!collapsed)}>
          {collapsed ? "»" : "«"}
        </button>
      </div>

      <nav className="sidebar-nav">
        {NAV_ITEMS.map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            className={({ isActive }) => "sidebar-link" + (isActive ? " active" : "")}
            title={collapsed ? item.label : undefined}
          >
            <span className="sidebar-icon">{item.icon}</span>
            {!collapsed && <span>{item.label}</span>}
          </NavLink>
        ))}
      </nav>

      <div className="sidebar-bottom">
        <button className="sidebar-logout" onClick={toggleDarkMode} title={collapsed ? "Toggle theme" : undefined}>
          <span className="sidebar-icon">{darkMode ? "☀️" : "🌙"}</span>
          {!collapsed && <span>{darkMode ? "Light mode" : "Dark mode"}</span>}
        </button>
        <button className="sidebar-logout" onClick={handleLogout} title={collapsed ? "Log out" : undefined}>
          <span className="sidebar-icon">🚪</span>
          {!collapsed && <span>Log out</span>}
        </button>
      </div>
    </aside>
  );
}

export default Sidebar;
