import React, { Component } from 'react';
import MainHeader from './Main_Header';
import Recipe from './Recipe';

class Favourites extends Component {
  render() {
    return (
      <div>
        <MainHeader />
        <div className="main_container">
          <div className="centered">
            <h1>My Favourites</h1>
          </div>
          <Recipe />
        </div>
      </div>
    );
  }
}

export default Favourites;
