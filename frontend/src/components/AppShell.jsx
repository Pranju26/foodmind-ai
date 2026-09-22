import Sidebar from "./Sidebar";
import "./AppShell.css";

function AppShell({ title, subtitle, children }) {
  return (
    <div className="app-shell">
      <Sidebar />
      <div className="app-shell-main">
        <header className="app-shell-header">
          <div>
            <h1>{title}</h1>
            {subtitle && <p>{subtitle}</p>}
          </div>
          <div className="app-shell-ai-status">
            <span className="ai-status-dot"></span>
            AI Nutrition Coach Online
          </div>
        </header>
        <div className="app-shell-content">{children}</div>
      </div>
    </div>
  );
}

export default AppShell;
