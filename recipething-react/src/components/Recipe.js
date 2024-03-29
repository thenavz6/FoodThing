import React, { Component } from 'react';
import { NavLink } from 'react-router-dom'
import GoogleLogo from '../images/Google.png';
import OpenStar from '../images/open_star.png';
import ClosedStar from '../images/closed_star.png';
import './Recipe.css'

class Recipe extends Component {
  render() {
    return (
      <div className="recipe_container">
        <div className="recipe">
          <img src={GoogleLogo} alt="GoogleLogo" className="recipeimage"/>
          <div className="overallrecipeinfo">
            <div className="recipeinfo1">
              <div className="recipetitle">
                <NavLink to="/view_recipe" className="navlink">
                  TWO DESSERTS, ONE CUP
                </NavLink>
              </div>
              <div className="recipefavourite">
                <img src={OpenStar} alt="OpenStar" height="40" width="40"/>
              </div>
            </div>
            <div className="recipeinfo2">
              <div className="recipetime">
                15 MIN
              </div>
            </div>
            <div className="recipeinfo1">
              <div className="reciperating">
                <img src={ClosedStar} alt="ClosedStar" height="40" width="40"/>
                <img src={ClosedStar} alt="ClosedStar" height="40" width="40"/>
                <img src={ClosedStar} alt="ClosedStar" height="40" width="40"/>
                <img src={ClosedStar} alt="ClosedStar" height="40" width="40"/>
                <img src={ClosedStar} alt="ClosedStar" height="40" width="40"/>
              </div>
              <div className="recipeprice">
                $12.00
              </div>
            </div>
            <div className="recipeinfo2">
              <div className="recipekeywords">
                DESSERT, ICECREAM, CHOCOLATE, DRINK
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default Recipe;
