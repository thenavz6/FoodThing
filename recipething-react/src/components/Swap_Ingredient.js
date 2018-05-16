import React, { Component } from 'react';
import Popup from "reactjs-popup";
import './Swap_Ingredient.css';
import './View_Recipe.css';
import GoogleLogo from '../images/Google.png';

class SwapIngredient extends Component {
  render() {
    return (
      <Popup trigger={<div className="swapbt"><button>SWAP</button></div>} modal closeOnDocumentClick>
        <span>
          <div className="green_background">
            <div className="swap_heading">
              INGREDIENT SWAP
            </div>
            <hr/>
            <div className="indent">
              <div className="swap_subheading">
                STORE
              </div>
              <div className="store_options">
                <div className="store_option">
                  Aldi
                </div>
                <div className="store_option">
                  Coles
                </div>
                <div className="store_option">
                  Woolworths
                </div>
              </div>
              <div className="swap_subheading">
                INGREDIENT
              </div>
              <div className="ingredient_search">
                <div className="ingredient_search_box">
                  <textarea name="comment" className="ingredient_box" placeholder="Enter the name of an ingredient to search..."/>
                </div>
                <input type="submit" value="Submit" name="ingredient_bt" className="ingredientbt"/>
              </div>
              <table className="ingredient_option_list">
                <tbody>
                  <tr>
                    <td className="ingredient_option">
                      <img src={GoogleLogo} alt="GoogleLogo" height="150" width="150"/>
                      <div className="ingredient_price">
                        $2.00
                      </div>
                    </td>
                    <td className="ingredient_option">
                      <img src={GoogleLogo} alt="GoogleLogo" height="150" width="150"/>
                      <div className="ingredient_price">
                        $0.72
                      </div>
                    </td>
                    <td className="ingredient_option">
                      <img src={GoogleLogo} alt="GoogleLogo" height="150" width="150"/>
                      <div className="ingredient_price">
                        $2.95
                      </div>
                    </td>
                    <td className="ingredient_option">
                      <img src={GoogleLogo} alt="GoogleLogo" height="150" width="150"/>
                      <div className="ingredient_price">
                        $1.50
                      </div>
                    </td>
                    <td className="ingredient_option">
                      <img src={GoogleLogo} alt="GoogleLogo" height="150" width="150"/>
                      <div className="ingredient_price">
                        $10.00
                      </div>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </span>
      </Popup>
    );
  }
}

export default SwapIngredient;
