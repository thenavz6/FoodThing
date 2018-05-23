import React, { Component } from 'react';
import './View_Recipe.css';

class IngredientDetails extends Component {
  render() {
    return (
        <td>
          <div className="ingredient_cell">
            1 Cheesecake
          </div>
        </td>
        <td>
          <div className="ingredient_cell">
            $8.95
          </div>
        </td>
        <td>
          <div className="ingredient_cell">
            BigCake
          </div>
        </td>
        <td className="swapbt">
          SWAP
        </td>
    );
  }
}

export default IngredientDetails;
