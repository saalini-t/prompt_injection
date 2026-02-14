import React from 'react';
import {
  Header,
  HeaderName,
  HeaderGlobalBar,
  HeaderGlobalAction,
  Theme
} from '@carbon/react';
import {
  Notification,
  UserAvatar,
  Switcher
} from '@carbon/icons-react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MultimodalScanner from './components/MultimodalScanner';
import './App.scss';

function App() {
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

        <div className="content-expanded">
          <Routes>
            <Route path="/" element={<MultimodalScanner />} />
            <Route path="*" element={<MultimodalScanner />} />
          </Routes>
        </div>
      </Router>
    </Theme>
  );
}

export default App;
