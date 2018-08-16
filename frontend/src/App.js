import React, { Component } from 'react';
import { BrowserRouter, Route, Switch } from 'react-router-dom';

import Home from './components/Home';

class App extends Component {
    render() {
        return (
            <div className="content">
                <BrowserRouter>
                    <Switch>
                        <Route path="/" component={Home} exact />
                    </Switch>
                </BrowserRouter> 
            </div>
     
        );
    }
}

export default App;
