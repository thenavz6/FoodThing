import React, { Component } from 'react';
import { NavLink } from 'react-router-dom';
import MainHeader from './Main_Header';
import './Dashboard.css';
import GoogleLogo from '../images/Google.png';
import OpenStar from '../images/open_star.png';

class Dashboard extends Component {
  render() {
    return (
      <div>
        <MainHeader />
        <div className="main_container">
          <div className="recipe_container">
            <div className="recipe">
            <img src={GoogleLogo} alt="GoogleLogo" className="recipeimage"/>
              <div className="overallrecipeinfo">
			      <div className="recipeinfo1">
			        <div className="recipetitle">
			          TWO DESSERTS, ONE CUP
			        </div>
			        <div className="recipefavourite">
			          <img src={OpenStar} alt="OpenStar" height="40" width="40"/>
			        </div>
			      </div><br/>
			      <div className="recipeinfo2">
			        <div className="recipetime">
			          15 MIN
			        </div>
			      </div>
			      <div className="recipeinfo">
			        <div className="reciperating">
			          <img src={OpenStar} alt="OpenStar" height="40" width="40"/>
			          <img src={OpenStar} alt="OpenStar" height="40" width="40"/>
			          <img src={OpenStar} alt="OpenStar" height="40" width="40"/>
			          <img src={OpenStar} alt="OpenStar" height="40" width="40"/>
			          <img src={OpenStar} alt="OpenStar" height="40" width="40"/>
		            </div>
		            <div className="recipeprice">
			          $12.00
			        </div>
			      </div>
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
                <img src={OpenStar} alt="OpenStar" className="recipestar"/>
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
                <img src={OpenStar} alt="OpenStar" className="recipestar"/>
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
                <img src={OpenStar} alt="OpenStar" className="recipestar"/>
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
                <img src={OpenStar} alt="OpenStar" className="recipestar"/>
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
