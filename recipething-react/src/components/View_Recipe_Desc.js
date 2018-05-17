import React, { Component } from 'react';
import OpenStar from '../images/open_star.png';
import ClosedStar from '../images/closed_star.png';
import './View_Recipe_Desc.css';
import GoogleLogo from '../images/Google.png';

class View_Recipe_Desc extends Component {
  render() {
    return (
      <div className="recipe_container">
        <div className="recipe">
          <div className="recipe_info">
            <div className="recipeinfo1">
              <div className="recipe_name">
                TWO DESSERTS, ONE CUP
              </div>
              <div className="recipefavourite">
                <img src={OpenStar} alt="OpenStar" height="40" width="40"/>
              </div>
            </div>
            <div className="recipeinfo1">
              <div className="recipe_author">
                By RadicalHipster
              </div>
              <div className="recipefavourite">
                <img src={ClosedStar} alt="ClosedStar" height="40" width="40"/>
                <img src={ClosedStar} alt="ClosedStar" height="40" width="40"/>
                <img src={ClosedStar} alt="ClosedStar" height="40" width="40"/>
                <img src={ClosedStar} alt="ClosedStar" height="40" width="40"/>
                <img src={ClosedStar} alt="ClosedStar" height="40" width="40"/>
              </div>
            </div>
            <div className="recipe_image_desc">
              <div className="recipe_image">
                <img src={GoogleLogo} alt="GoogleLogo" height="200" width="200"/>
              </div>
              <div className="right_desc">
                <div className="recipeinfo1">
                  <div className="recipe_subheading">
                    DESCRIPTION
                  </div>
                  <div className="recipe_time">
                    15 MIN
                  </div>
                </div>
                <div className="recipe_desc">
                  This recipe is all about icecream in cones. Delicious, if I do say so myself! If you like icecream, you will love this recipe! #delicious #icecream #goodness #healthyliving
                </div>
                <div className="recipeinfo1">
                  <div className="recipe_calories">
                    30,000 CALORIES
                  </div>
                  <div className="recipeprice">
                    $12.00
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

export default View_Recipe_Desc;
