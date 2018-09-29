import React, { Component } from 'react';
import createBrowserHistory from 'history/createBrowserHistory';
import { BrowserRouter, Route, Switch } from 'react-router-dom';
import { Provider } from 'react-redux';

import Home from './components/pages/Home';
import Problems from './components/pages/Problems';
import Problem from './components/pages/Problem';
import NotFound from './components/pages/NotFound';
import Login from './components/pages/Login';
import Register from './components/pages/Register';

import loadScript from 'load-script';
import store from './store';

const MATHJAX_SCRIPT = 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-MML-AM_CHTML';
const MATHJAX_OPTIONS = {
    text2jax: {
        inlineMath: [['$', '$'], ['\\(', '\\)']],
        displayMath: [['$$', '$$'], ['\[', '\]']]
    },
    showMathMenu: false,
    showMathMenuMSIE: false
}

export default class App extends Component {
    constructor(props) {
        super(props);
        loadScript(MATHJAX_SCRIPT, () => {
            window.MathJax.Hub.Config(MATHJAX_OPTIONS);
        });
    }

    render() {
        return (
            <Provider store={store}>
                <BrowserRouter>
                    <Switch>
                        <Route path="/" component={Home} exact />
                        <Route path="/login" component={Login} exact />
                        <Route path="/register" component={Register} exact />
                        <Route path="/problems" component={Problems} exact />
                        <Route path="/contests" component={Home} exact />
                        <Route path="/ranks" component={Home} exact />
                        <Route path="/about" component={Home} exact />
                        <Route path="/problem/:id" component={Problem} exact />
                        <Route path="*" component={NotFound} />
                    </Switch>
                </BrowserRouter>
            </Provider>
        );
    }
}