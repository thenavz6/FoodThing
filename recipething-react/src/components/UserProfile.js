import React, { Component } from 'react';
import MainHeader from './Main_Header';
import ProfileDesc from './Profile_Desc';
import Recipe from './Recipe';

class UserProfile extends Component {
  render() {
    return (
      <div>
        <MainHeader />
        <div className="main_container">
          <ProfileDesc/>
          <div className="profile_heading">
            {/*Need to be either "Favourites" or "Your Favourites" depending on user*/}
            YOUR FAVOURITES
          </div>
          {/*Need to check if user has favourited any recipes, otherwise blank?*/}
          <Recipe/>
          <div className="profile_heading">
            {/*Need to be either "Recipes" or "Your Recipes" depending on user*/}
            YOUR RECIPES
          </div>
          <Recipe/>
        </div>
      </div>
    );
  }
}

export default UserProfile;
