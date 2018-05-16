import React, { Component } from 'react';

class RecipeCommentReply extends Component {
  render() {
    return (
      <div className="recipe_container">
        <div className="recipe">
          <div className="recipe_reply">
            <div className="recipe_subheading">
              REPLY
            </div>
            <textarea name="comment" className="commentbox" placeholder="Add your comment here..."/>
            <input type="submit" value="Submit" name="reply_bt" className="searchbt"/>
          </div>
        </div>
      </div>
    );
  }
}

export default RecipeCommentReply;
