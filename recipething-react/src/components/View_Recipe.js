import React, { Component } from 'react';
import MainHeader from './Main_Header';
import ViewRecipeDesc from './View_Recipe_Desc';
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
                  <td>
                    1 Cheesecake
                  </td>
                  <td>
                    $8.95
                  </td>
                  <td>
                    BigCake
                  </td>
                  <td className="swapbt">
                    SWAP
                  </td>
                </tr>
                <tr>
                  <td>
                    1L Milk
                  </td>
                  <td>
                    $1.50
                  </td>
                  <td>
                    Walmart
                  </td>
                  <td className="swapbt">
                    SWAP
                  </td>
                </tr>
                <tr>
                  <td>
                    1L Milkshake Mix
                  </td>
                  <td>
                    $1.55
                  </td>
                  <td>
                    Kelis
                  </td>
                  <td className="swapbt">
                    SWAP
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
          <div className="recipe_container">
            <div className="recipe">
              COMMENT
            </div>
          </div>
          <div className="recipe_container">
            <div className="recipe">
              COMMENT
            </div>
          </div>
          <div className="recipe_container">
            <div className="recipe">
              <div className="recipe_comment">
                <div className="recipe_subheading">
                  REPLY
                </div>
                <textarea name="comment" className="commentbox" placeholder="Add your comment here..."/>
                <input type="submit" value="Submit" name="reply_bt" className="searchbt"/>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default ViewRecipe;
