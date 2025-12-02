import React from "react";

export function TradesTable({ trades }) {
  if (!trades || trades.length === 0) {
    return <div className="placeholder">Нет сделок</div>;
  }

  return (
    <div className="table-wrapper">
      <table>
        <thead>
          <tr>
            <th>Type</th>
            <th>Entry Date</th>
            <th>Entry Price</th>
            <th>Exit Date</th>
            <th>Exit Price</th>
            <th>Return %</th>
          </tr>
        </thead>
        <tbody>
          {trades.map((t, idx) => {
            const ret = t.return;
            let cls = "value-neutral";
            if (ret != null) {
              if (ret > 0) cls = "value-positive";
              else if (ret < 0) cls = "value-negative";
            }

            return (
              <tr key={idx}>
                <td>{t.type}</td>
                <td>{t.entry_date}</td>
                <td>{t.entry_price?.toFixed(2)}</td>
                <td>{t.exit_date}</td>
                <td>{t.exit_price?.toFixed(2)}</td>
                <td className={cls}>
                  {ret != null ? `${(ret * 100).toFixed(2)}%` : ""}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}


