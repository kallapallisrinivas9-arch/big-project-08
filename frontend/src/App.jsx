import React from "react";

import Dashboard from "./components/Dashboard";

export default function App() {
  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#07130d",
        color: "#f5f7f5",
        fontFamily:
          "Inter, Arial, sans-serif",
      }}
    >
      <Dashboard />
    </div>
  );
}