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
              <div className="add_recipe_columns">
                <div className="add_recipe_subheading_column">
                  Recipe Name:
                </div>
                <div className="add_recipe_subheading_column">
                  Time Required:
                </div>
              </div>
              <div className="add_recipe_columns">
                <textarea name="recipe_name_text" className="add_recipe_box" placeholder="Enter the recipe name..."/>
                <textarea name="time_required_text" className="add_recipe_box" placeholder="Enter the time required..."/>
              </div>
              <div className="add_recipe_subheading">
                Description:
              </div>
              <textarea name="recipe_desc_text" className="add_recipe_box2" placeholder="Enter the recipe description..."/>
              <div className="add_recipe_subheading">
                Recipe Image:
              </div>
              <textarea name="recipe_image_text" className="add_recipe_box3" placeholder="Enter the image URL here..."/>
              <div className="add_recipe_subheading">
                Recipe Ingredients:
              </div>
              <textarea name="recipe_ingredients_text" className="add_recipe_box3" placeholder="Enter the recipe's ingredients here..."/>
              <div className="add_recipe_subheading">
                Recipe Instructions:
              </div>
              <textarea name="recipe_instructions_text" className="add_recipe_box3" placeholder="Enter the recipe's instructions here..."/>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default AddRecipe;
