import React, { Component } from 'react';
import HomeHeader from './components/Home_Header';
import logo from './images/logo.png';
import GoogleLogo from  './images/Google.png';
import FacebookLogo from  './images/Facebook.png';
import './App.css';

class App extends Component {
  render() {
    return (
      <div className="App">
        <HomeHeader />
        <div className="homepage_body">
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
                        <img src={GoogleLogo} alt="GoogleLogo" className="auth_logo"/>
                    </div>
                    <div className="auth_img_button">
                        <img src={FacebookLogo} alt="FacebookLogo" className="auth_logo"/>
                    </div>
                    <div className="auth_button">Continue as GUEST</div>
                </div>
            </div>
        </div>
      </div>
    );
  }
}

export default App;
