import React, { Component } from 'react';
import './Profile_Desc.css';
import GoogleLogo from '../images/Google.png';

class Profile_Desc extends Component {
  render() {
    return (
      <div className="profile_container">
        <div className="profile">
          <div className="profile_info">
            <div className="profile_name">
              TOM BOB
            </div>
            <div className="profile_image_desc">
              {/*Need a default image for new user profiles*/}
              <div className="profile_image">
                <img src={GoogleLogo} alt="GoogleLogo" height="200" width="200"/>
              </div>
              <div className="right_desc">
                <div className="profile_subheading">
                  DESCRIPTION:
                </div>
                <div className="profile_desc">
                  I love absorbing nutrients by inserting edible items into my face.
                </div>
              </div>
            </div>
          </div>
          {/*This button should only be available to the relevant user*/}
          <div className="editbt">
            {/*Need to add ability to edit profile description*/}
            EDIT
          </div>
        </div>
      </div>
    );
  }
}

export default Profile_Desc;
