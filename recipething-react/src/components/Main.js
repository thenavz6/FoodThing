import React from 'react';
import { Switch, Route } from 'react-router-dom';
import HomePage from './Home';
import About from './About';

const Main = () => (
  <main>
    <Switch>
      <Route exact path='/' component={HomePage}/>
      <Route path='/dashboard' component={Dashboard}/>
    </Switch>
  </main>
);

export default Main;
