# SentinelAI SOC Dashboard

Professional Security Operations Center dashboard built with React and IBM Carbon Design System.

## Features

- 📊 Real-time threat monitoring
- 📈 Attack analytics and visualization
- 🔴 Live attack feed via WebSocket
- 📋 Attack logs with filtering
- ⚙️ Policy management interface
- 💚 System health monitoring
- 🎨 IBM Carbon Design System components
- 🌓 Dark theme optimized for SOC operations

## Tech Stack

- **React 18** - UI framework
- **IBM Carbon Design System** - UI components
- **Recharts** - Data visualization
- **Vite** - Build tool
- **Axios** - HTTP client
- **React Router** - Navigation

## Installation

```bash
cd sentinelai_dashboard
npm install
```

## Development

```bash
npm run dev
```

Dashboard will be available at http://localhost:3000

## Build

```bash
npm run build
```

## Backend Integration

The dashboard connects to your SentinelAI backend:
- API: http://127.0.0.1:8000/api/v1/*
- WebSocket: ws://127.0.0.1:8000/ws

Make sure your backend server is running before starting the dashboard.

## Pages

1. **Dashboard** - Overview with metrics, charts, and live feed
2. **Attack Logs** - Detailed attack history with filtering
3. **Policies** - Policy configuration and management
4. **System Health** - Component status and uptime monitoring

## Components

- `MetricsCard` - KPI display cards
- `ThreatChart` - 24-hour threat activity visualization
- `LiveFeed` - Real-time attack event stream
- `SideNav` - Navigation sidebar

## Configuration

Proxy settings in `vite.config.js` route API calls to your backend:

```javascript
proxy: {
  '/api': 'http://127.0.0.1:8000',
  '/ws': 'ws://127.0.0.1:8000'
}
```
