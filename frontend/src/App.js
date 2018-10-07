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
import Settings from './components/pages/Settings';

import loadScript from 'load-script';
import store from './store';
import setAuthorizationToken from './utils/setAuthorizationToken';
import jwt from 'jsonwebtoken';
import axios from 'axios';

import { userLogout } from './actions/authenticationActions';

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

    componentWillMount() {
        this.createVerifyTokenInterceptor();
        setAuthorizationToken(localStorage.access_token);
    }

    createVerifyTokenInterceptor() {
        this.verifyTokenInterceptor = axios.interceptors.request.use((config) => {
            const accessToken = localStorage.access_token;
            const refreshToken = localStorage.refresh_token;

            if (accessToken && refreshToken) {
                const decodedToken = jwt.decode(accessToken);
                if (!decodedToken) return config;

                const dateNow = new Date();
    
                const isExpired = decodedToken.exp < dateNow.getTime() / 1000;
                if (isExpired) {
                    axios.interceptors.request.eject(this.verifyTokenInterceptor);

                    // Access Token is expired
                    // Send a request for a new access
                    // token using the refresh token
                    axios.get('http://localhost:5000/api/users/authenticate/refresh', {
                        headers: {
                            'Authorization': 'Bearer ' + refreshToken
                        }
                    }).then((res) => {
                        const newToken = res.access_token;
                        localStorage.setItem('access_token', newToken);
                        setAuthorizationToken(newToken); 
                        this.createVerifyTokenInterceptor();

                    }).catch((error) => {
                        console.log(error);
                        store.dispatch(userLogout());
                        this.createVerifyTokenInterceptor();
                    });
                }
    
                console.log('isExpired: ' + isExpired);
            }
    
            return config;
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
                        <Route path="/settings" component={Settings} exact />
                        <Route path="*" component={NotFound} />
                    </Switch>
                </BrowserRouter>
            </Provider>
        );
    }
}