import React, { Component } from 'react';
import { NavLink } from 'react-router-dom';
import HomeHeader from './Home_Header';
import GoogleLogo from  '../images/Google.png';
import FacebookLogo from  '../images/Facebook.png';
import logo from '../images/logo.png';
import './Home.css';

class Home extends Component {
  render(){
    return (
      <div>
        <HomeHeader />
        <div className="main_container">
          <div className="logo_container">
              <img src={logo} alt="logo" className="logo"/>
          </div>
          <div className="centered">
            <h1>Welcome to RecipeThing!</h1>
            <h2>Please login using one of the following options:</h2>
          </div>
          <div className="button_block">
            <div className="auth_img_button">
              <NavLink to="/dashboard"><img src={GoogleLogo} alt="GoogleLogo" className="auth_logo"/></NavLink>
            </div>
            <div className="auth_img_button">
              <NavLink to="/dashboard"><img src={FacebookLogo} alt="FacebookLogo" className="auth_logo"/></NavLink>
            </div>
            <div className="auth_button">
              <NavLink className="navlink" to="/dashboard">Continue as GUEST</NavLink>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default Home;
