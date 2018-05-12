import React, { Component } from 'react';
import MainHeader from './Main_Header';
import Recipe from './Recipe';
import './Dashboard.css';

class UserProfile extends Component {
  render() {
    return (
      <div>
        <MainHeader />
        <div className="main_container">
          <div className="recipe_container">
            <div className="recipe">
              <h1>TOM BOB</h1>
              <h1>YOUR RECIPES</h1>
              <h1>YOUR FAVOURITES</h1>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default UserProfile;
