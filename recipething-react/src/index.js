import React from 'react';
import ReactDOM from 'react-dom';
import {
  BrowserRouter as Router,
  Route
} from 'react-router-dom';
import Home from './components/Home';
import Dashboard from './components/Dashboard';
import Favourites from './components/Favourites';
import UserProfile from './components/UserProfile';
import './index.css';

ReactDOM.render(
  <Router>
    <div className="index">
      <Route exact path="/" component={Home}/>
      <Route path="/dashboard" component={Dashboard}/>
      <Route path="/favourites" component={Favourites}/>
      <Route path="/profile" component={UserProfile}/>
      <Route path="/profile/edit" component={UserProfile}/>
    </div>
  </Router>,
  document.getElementById('root')
);
