import React, { Component } from 'react';
import MainHeader from './Main_Header';
import Recipe from './Recipe';
import OpenStar from '../images/open_star.png';

class Favourites extends Component {
  render() {
    return (
      <div>
        <MainHeader />
        <div className="main_container">
          {/*This should only appear if a registered user has no favourites.*/}
          <div className="loggedin">
            <div className="centered">
              <h2>Click (<img src={OpenStar} alt="OpenStar" height="40" width="40"/>) to add recipes to your favourites.</h2>
            </div>
          </div>
          <div className="notloggedin">
            <div className="centered">
              <h1>My Favourites</h1>
            </div>
          <Recipe />
          </div>
        </div>
      </div>
    );
  }
}

export default Favourites;
