import React, { Component } from 'react';
import './Swap_Ingredient.css';

class SwapIngredient extends Component {
  render() {
    return (
      <div className="green_background">
        <div className="swap_heading">
          INGREDIENT SWAP
        </div>
        <hr/>
        <div className="indent">
          <div className="swap_subheading">
            STORE
          </div>
          <div className="store_dropdown">
            Drop Down Menu
          </div>
          <div className="swap_subheading">
            INGREDIENT
          </div>
        </div>
      </div>
    );
  }
}

export default SwapIngredient;
