import React, { Component } from 'react';
import Navigation from './Navigation';

class Home extends Component {
    componentDidMount() {
        document.title = "Home - Online Grader";
    }

    render() {
        return (
            <Navigation />
        );
    }
}

export default Home;