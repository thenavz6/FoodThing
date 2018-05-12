import React, { Component } from 'react';
import { NavLink } from 'react-router-dom';
import MainHeader from './Main_Header';
import Recipe from './Recipe';
import './Dashboard.css';

class Dashboard extends Component {
  render() {
    return (
      <div>
        <MainHeader />
        <div className="main_container">
          <Recipe />
          <Recipe />
          <Recipe />
          <Recipe />
          <Recipe />
          <div className="favourites_button">
            <NavLink className="navlink" to="/">My Favourites</NavLink>
          </div>
        </div>
      </div>
    );
  }
}

export default Dashboard;
