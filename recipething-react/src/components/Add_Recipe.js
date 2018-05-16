import React, { Component } from 'react';
import MainHeader from './Main_Header';
import './Add_Recipe.css';

class AddRecipe extends Component {
  render() {
    return (
      <div>
        <MainHeader/>
        <div className="main_container">
          <div className="add_recipe_heading">
            ADD RECIPE
          </div>
          <div className="add_recipe_info_container">
            <div className="add_recipe_info">
              <div className="recipeinfo1">
                <div className="add_recipe_subheading">
                  Recipe Name:
                </div>
                <div className="add_recipe_subheading2">
                  Time Required:
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default AddRecipe;
