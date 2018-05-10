import React, { Component } from 'react';
import { NavLink } from 'react-router-dom';
import MainHeader from './Main_Header';
import './Dashboard.css';
import GoogleLogo from '../images/Google.png';

class Dashboard extends Component {
  render() {
    return (
      <div>
        <MainHeader />
        <div className="main_container">
          <div className="recipe_container">
            <div className="recipe">
            <img src={GoogleLogo} alt="GoogleLogo" className="recipeimage"/>
              <div className="recipetitle">
                TWO DESSERTS, ONE CUP
              </div>
              <img src={GoogleLogo} alt="GoogleLogo" className="recipestar"/>
              <div className="recipetime">
                15 MIN
              </div>
            </div>
          </div>
          <div className="recipe_container">
            <div className="recipe">
              <img src={GoogleLogo} alt="GoogleLogo" className="recipeimage"/>
              <div className="recipetitleinfo">
                <div className="recipetitle">
                  O SUBWAY
                </div>
                <img src={GoogleLogo} alt="GoogleLogo" className="recipestar"/>
              </div>
            </div>
          </div>
          <div className="recipe_container">
            <div className="recipe">
              <img src={GoogleLogo} alt="GoogleLogo" className="recipeimage"/>
              <div className="recipetitleinfo">
                <div className="recipetitle">
                  HEART ATTACK IN A BOWL
                </div>
                <img src={GoogleLogo} alt="GoogleLogo" className="recipestar"/>
              </div>
              <div className="recipetime">
                15 MIN
              </div>
            </div>
          </div>
          <div className="recipe_container">
            <div className="recipe">
              <img src={GoogleLogo} alt="GoogleLogo" className="recipeimage"/>
              <div className="recipetitleinfo">
                <div className="recipetitle">
                  RECIPE 4
                </div>
                <img src={GoogleLogo} alt="GoogleLogo" className="recipestar"/>
              </div>
              <div className="recipetime">
                15 MIN
              </div>
            </div>
          </div>
          <div className="recipe_container">
            <div className="recipe">
              <img src={GoogleLogo} alt="GoogleLogo" className="recipeimage"/>
              <div className="recipetitleinfo">
                <div className="recipetitle">
                  RECIPE 5
                </div>
                <img src={GoogleLogo} alt="GoogleLogo" className="recipestar"/>
              </div>
              <div className="recipetime">
                15 MIN
              </div>
            </div>
          </div>
          <div className="favourites_button">
            <NavLink className="navlink" to="/">My Favourites</NavLink>
          </div>
        </div>
      </div>
    );
  }
}

export default Dashboard;
