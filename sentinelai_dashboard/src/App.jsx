import React, { useState } from 'react';
import {
  Header,
  HeaderName,
  HeaderGlobalBar,
  HeaderGlobalAction,
  Theme,
  Content
} from '@carbon/react';
import {
  Notification,
  UserAvatar,
  Switcher
} from '@carbon/icons-react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import AttackLogs from './pages/AttackLogs';
import PolicyManager from './pages/PolicyManager';
import SystemHealth from './pages/SystemHealth';
import SideNav from './components/SideNav';
import './App.scss';

function App() {
  const [isSideNavExpanded, setIsSideNavExpanded] = useState(true);

  return (
    <Theme theme="white">
      <Router>
        <Header aria-label="SentinelAI SOC">
          <HeaderName href="/" prefix="SentinelAI">
            Security Operations Center
          </HeaderName>
          <HeaderGlobalBar>
            <HeaderGlobalAction aria-label="Notifications" tooltipAlignment="end">
              <Notification size={20} />
            </HeaderGlobalAction>
            <HeaderGlobalAction aria-label="User Profile" tooltipAlignment="end">
              <UserAvatar size={20} />
            </HeaderGlobalAction>
            <HeaderGlobalAction aria-label="App Switcher" tooltipAlignment="end">
              <Switcher size={20} />
            </HeaderGlobalAction>
          </HeaderGlobalBar>
        </Header>

        <SideNav 
          isExpanded={isSideNavExpanded}
          onToggle={() => setIsSideNavExpanded(!isSideNavExpanded)}
        />

        <Content className={isSideNavExpanded ? 'content-expanded' : 'content-collapsed'}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/attacks" element={<AttackLogs />} />
            <Route path="/policies" element={<PolicyManager />} />
            <Route path="/health" element={<SystemHealth />} />
          </Routes>
        </Content>
      </Router>
    </Theme>
  );
}

export default App;
