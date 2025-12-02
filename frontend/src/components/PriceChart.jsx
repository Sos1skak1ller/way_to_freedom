import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Scatter
} from "recharts";

export function PriceChart({ price, labels, signals, theme = "light" }) {
  if (!price || price.length === 0) {
    return <div className="placeholder">Нет данных цены</div>;
  }

  const data = price.map((p, i) => ({
    date: labels[i],
    price: p,
    signal: signals?.[i] ?? 0
  }));

  const isDark = theme === "dark";

  return (
    <ResponsiveContainer width="100%" height={260}>
      <LineChart data={data} margin={{ top: 10, right: 10, left: 12, bottom: 0 }}>
        <XAxis dataKey="date" hide />
        <YAxis domain={["auto", "auto"]} />
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
        <Line
          type="monotone"
          dataKey="price"
          stroke="var(--text)"
          strokeWidth={1.5}
          dot={false}
        />
        <Scatter dataKey="price" data={data.filter((d) => d.signal === 1)} fill="#16a34a" />
        <Scatter dataKey="price" data={data.filter((d) => d.signal === -1)} fill="#dc2626" />
      </LineChart>
    </ResponsiveContainer>
  );
}


