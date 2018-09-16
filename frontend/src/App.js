import React, { Component } from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';

import Home from './components/pages/Home';
import Problems from './components/pages/Problems';
import Problem from './components/pages/Problem';
import NotFound from './components/pages/NotFound';

export default class App extends Component {
  render() {
    return (
      <BrowserRouter>
        <Switch>
          <Route path="/" component={Home} exact />
          <Route path="/problems" component={Problems} exact />
          <Route path="/contests" component={Home} exact />
          <Route path="/ranks" component={Home} exact />
          <Route path="/about" component={Home} exact />
          <Route path="/problem/:id" component={Problem} exact />
          <Route path="*" component={NotFound} />
        </Switch>
      </BrowserRouter>
    );
  }
}