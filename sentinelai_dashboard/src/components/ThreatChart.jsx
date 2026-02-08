import React, { useState, useEffect } from 'react';
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const ThreatChart = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    // Generate mock data for the last 24 hours
    const hours = 24;
    const mockData = [];
    const now = new Date();

    for (let i = hours; i >= 0; i--) {
      const time = new Date(now.getTime() - i * 60 * 60 * 1000);
      mockData.push({
        time: time.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' }),
        blocked: Math.floor(Math.random() * 15) + 2,
        sanitized: Math.floor(Math.random() * 20) + 5,
        allowed: Math.floor(Math.random() * 50) + 30
      });
    }

    setData(mockData);
  }, []);

  return (
    <ResponsiveContainer width="100%" height={300}>
      <AreaChart data={data}>
        <defs>
          <linearGradient id="colorBlocked" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#da1e28" stopOpacity={0.8}/>
            <stop offset="95%" stopColor="#da1e28" stopOpacity={0}/>
          </linearGradient>
          <linearGradient id="colorSanitized" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#f1c21b" stopOpacity={0.8}/>
            <stop offset="95%" stopColor="#f1c21b" stopOpacity={0}/>
          </linearGradient>
          <linearGradient id="colorAllowed" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#24a148" stopOpacity={0.8}/>
            <stop offset="95%" stopColor="#24a148" stopOpacity={0}/>
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
        <XAxis dataKey="time" stroke="#525252" />
        <YAxis stroke="#525252" />
        <Tooltip 
          contentStyle={{ backgroundColor: '#ffffff', border: '1px solid #e0e0e0', borderRadius: '4px' }}
          labelStyle={{ color: '#161616' }}
        />
        <Legend />
        <Area type="monotone" dataKey="blocked" stroke="#da1e28" fillOpacity={1} fill="url(#colorBlocked)" />
        <Area type="monotone" dataKey="sanitized" stroke="#f1c21b" fillOpacity={1} fill="url(#colorSanitized)" />
        <Area type="monotone" dataKey="allowed" stroke="#24a148" fillOpacity={1} fill="url(#colorAllowed)" />
      </AreaChart>
    </ResponsiveContainer>
  );
};

export default ThreatChart;
