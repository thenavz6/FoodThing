import React from "react";
import { NavLink } from 'react-router-dom';
import SearchImage from '../images/search.png';
import NotificationsImage from '../images/notifications.png';
import './Header.css';

const MainHeader = () => (
    <nav className="navbar navbar-default navbar-fixed-top">
        <div className="navbar-container">
          <img src={SearchImage} alt="searchimage" className="searchimage"/>
          <div className="searchbox">Here goes the search box using react-search-box...</div>
          <div className="recipething">RECIPETHING</div>
          <NavLink to="/"><img src={NotificationsImage} alt="notifyimage" className="notifyimage"/></NavLink>
          <div className="rightbuttons">
            <NavLink className="navlink" to="/">ADD RECIPE</NavLink>
          </div>
          <div className="buttondivider">|</div>
          <div className="rightbuttons">
            <NavLink className="navlink" to="/">PROFILE</NavLink>
          </div>
          <div className="buttondivider">|</div>
          <div className="rightbuttons">
            <NavLink className="navlink" to="/">LOGOUT</NavLink>
          </div>
        </div>
    </nav>
)

export default MainHeader;
