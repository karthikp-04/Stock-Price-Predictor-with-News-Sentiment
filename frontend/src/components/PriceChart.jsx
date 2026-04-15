// src/components/PriceChart.jsx
import {
  AreaChart, Area, Line, XAxis, YAxis,
  CartesianGrid, Tooltip, ResponsiveContainer,
} from 'recharts';

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null;
  return (
    <div className="custom-tooltip">
      <div className="label">{label}</div>
      {payload.map((p, i) => (
        <div key={i} className="value" style={{ color: p.color }}>
          {p.name}: ${Number(p.value).toFixed(2)}
        </div>
      ))}
    </div>
  );
}

export default function PriceChart({ data, ticker }) {
  if (!data || data.length === 0) return null;

  return (
    <div className="card price-chart" id="price-chart">
      <h3>Price History — {ticker}</h3>

      <ResponsiveContainer width="100%" height={280}>
        <AreaChart data={data} margin={{ top: 8, right: 8, left: -8, bottom: 0 }}>
          <defs>
            <linearGradient id="gradClose" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%"  stopColor="#58a6ff" stopOpacity={0.25} />
              <stop offset="95%" stopColor="#58a6ff" stopOpacity={0} />
            </linearGradient>
          </defs>

          <CartesianGrid strokeDasharray="3 3" stroke="rgba(48,54,61,0.35)" />

          <XAxis
            dataKey="date"
            tick={{ fill: '#8b949e', fontSize: 11 }}
            tickFormatter={(v) => v.slice(5)}
            axisLine={{ stroke: 'rgba(48,54,61,0.5)' }}
          />
          <YAxis
            tick={{ fill: '#8b949e', fontSize: 11 }}
            domain={['auto', 'auto']}
            tickFormatter={(v) => `$${v}`}
            axisLine={{ stroke: 'rgba(48,54,61,0.5)' }}
          />

          <Tooltip content={<CustomTooltip />} />

          <Area
            type="monotone"
            dataKey="close"
            name="Close"
            stroke="#58a6ff"
            strokeWidth={2}
            fill="url(#gradClose)"
            dot={false}
            activeDot={{ r: 4, fill: '#58a6ff', stroke: '#0d1117', strokeWidth: 2 }}
          />
          <Line
            type="monotone"
            dataKey="ma5"
            name="MA 5"
            stroke="#d29922"
            strokeWidth={1.5}
            strokeDasharray="5 3"
            dot={false}
          />
          <Line
            type="monotone"
            dataKey="ma20"
            name="MA 20"
            stroke="#bc8cff"
            strokeWidth={1.5}
            strokeDasharray="5 3"
            dot={false}
          />
        </AreaChart>
      </ResponsiveContainer>

      <div className="chart-legend">
        <div className="legend-item">
          <span className="legend-line" style={{ background: '#58a6ff' }} />
          Close
        </div>
        <div className="legend-item">
          <span className="legend-line" style={{ background: '#d29922' }} />
          MA 5
        </div>
        <div className="legend-item">
          <span className="legend-line" style={{ background: '#bc8cff' }} />
          MA 20
        </div>
      </div>
    </div>
  );
}
