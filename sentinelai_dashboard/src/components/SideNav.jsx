import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  SideNav as CarbonSideNav,
  SideNavItems,
  SideNavLink
} from '@carbon/react';
import {
  Dashboard,
  SecurityServices,
  Report,
  Activity
} from '@carbon/icons-react';

const SideNav = ({ isExpanded, onToggle }) => {
  const navigate = useNavigate();
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Dashboard', icon: Dashboard },
    { path: '/attacks', label: 'Attack Logs', icon: SecurityServices },
    { path: '/policies', label: 'Policies', icon: Report },
    { path: '/health', label: 'System Health', icon: Activity }
  ];

  return (
    <CarbonSideNav
      aria-label="Side navigation"
      isFixedNav
      expanded={isExpanded}
      onOverlayClick={onToggle}
      isPersistent={false}
    >
      <SideNavItems>
        {navItems.map((item) => (
          <SideNavLink
            key={item.path}
            renderIcon={item.icon}
            onClick={() => navigate(item.path)}
            isActive={location.pathname === item.path}
          >
            {item.label}
          </SideNavLink>
        ))}
      </SideNavItems>
    </CarbonSideNav>
  );
};

export default SideNav;
