import React from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export function EquityChart({ equity, labels, theme = "light" }) {
  if (!equity || equity.length === 0) {
    return <div className="placeholder">Нет данных equity</div>;
  }

  const data = equity.map((v, i) => ({
    date: labels[i],
    equity: v
  }));

  const isDark = theme === "dark";

  return (
    <ResponsiveContainer width="100%" height={260}>
      <LineChart data={data} margin={{ top: 10, right: 10, left: 12, bottom: 0 }}>
        <XAxis dataKey="date" hide />
        <YAxis
          domain={["auto", "auto"]}
          tickFormatter={(v) => {
            if (v >= 1000 || v <= -1000) {
              return `${(v / 1000).toFixed(0)}k`;
            }
            return v.toFixed(0);
          }}
        />
        <Tooltip
          contentStyle={{
            backgroundColor: isDark ? "#020617" : "#ffffff",
            border: `1px solid ${isDark ? "#1e293b" : "#e5e7eb"}`,
            borderRadius: 8,
            fontSize: 12,
            color: isDark ? "#e5e7eb" : "#111827"
          }}
          labelStyle={{ color: isDark ? "#9ca3af" : "#6b7280", fontSize: 11 }}
          itemStyle={{ color: isDark ? "#e5e7eb" : "#111827" }}
        />
        <Line type="monotone" dataKey="equity" stroke="#4f46e5" strokeWidth={2} dot={false} />
      </LineChart>
    </ResponsiveContainer>
  );
}


