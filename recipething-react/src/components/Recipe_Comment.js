import React, { Component } from 'react';
import GoogleLogo from '../images/Google.png';

class RecipeComment extends Component {
  render() {
    return (
      <div className="recipe_container">
        <div className="recipe">
          <div className="profile_info">
            <div className="recipe_subheading">
              ILiveOffMinimumWage
            </div>
            <div className="profile_image_desc">
              {/*Need a default image for new user profiles*/}
              <div className="profile_image">
                <img src={GoogleLogo} alt="GoogleLogo" height="100" width="100"/>
              </div>
              <div className="right_desc">
                <div className="profile_desc">
                  Is this even edible?
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default RecipeComment;
