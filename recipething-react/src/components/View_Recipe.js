import React, { Component } from 'react';
import MainHeader from './Main_Header';
import ViewRecipeDesc from './View_Recipe_Desc';
import RecipeComment from './Recipe_Comment';
import RecipeCommentReply from './Recipe_Comment_Reply.js';
import SwapIngredient from './Swap_Ingredient';
import './View_Recipe.css';

class ViewRecipe extends Component {
  render() {
    return (
      <div>
        <MainHeader/>
        <div className="main_container">
          <ViewRecipeDesc/>
          <div className="recipe_heading">
            INGREDIENTS
          </div>
          <div className="list">
            <table className="ingredient_list">
              <tbody>
                <tr>
                  <td className="ingredient_list_element">
                    1 Cheesecake
                  </td>
                  <td className="ingredient_list_element">
                    $8.95
                  </td>
                  <td className="ingredient_list_element">
                    BigCake
                  </td>
                  <td className="ingredient_list_element">
                    <SwapIngredient/>
                  </td>
                </tr>
                <tr>
                  <td className="ingredient_list_element">
                    1L Milk
                  </td>
                  <td className="ingredient_list_element">
                    $1.50
                  </td>
                  <td className="ingredient_list_element">
                    Walmart
                  </td>
                  <td className="ingredient_list_element">
                    <SwapIngredient/>
                  </td>
                </tr>
                <tr>
                  <td className="ingredient_list_element">
                    1L Milkshake Mix
                  </td>
                  <td className="ingredient_list_element">
                    $1.55
                  </td>
                  <td className="ingredient_list_element">
                    Kelis
                  </td>
                  <td className="ingredient_list_element">
                    <SwapIngredient/>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
          <div className="recipe_heading">
            INSTRUCTIONS
          </div>
          <div className="list">
            <ol>
              <li>Make the milkshake.</li>
              <li>Shove a cheesecake on it.</li>
              <li>Stir.</li>
            </ol>
          </div>
          <div className="recipe_heading">
            COMMENTS
          </div>
          <RecipeComment/>
          <RecipeComment/>
          <RecipeCommentReply/>
        </div>
      </div>
    );
  }
}

export default ViewRecipe;
