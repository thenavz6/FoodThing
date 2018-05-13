import React, { Component } from 'react';
import MainHeader from './Main_Header';
import './UserProfile.css';
import GoogleLogo from '../images/Google.png';
import OpenStar from '../images/open_star.png';

class UserProfile extends Component {
  render() {
    return (
      <div>
        <MainHeader />
        <div className="main_container">
          <div className="profile_container">
            <div className="profile">
              <div className="profile_info">
                <div className="profile_name">
                  TOM BOB
                </div>
                <div className="profile_image_desc">
                  <div className="profile_image">
                    <img src={GoogleLogo} alt="GoogleLogo" height="250" width="250"/>
                  </div>
                  <div className="profile_heading">
                    DESCRIPTION:
                  </div>
                  <div className="profile_desc">
                    I love absorbing nutrients by inserting edible items into my face.
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default UserProfile;
