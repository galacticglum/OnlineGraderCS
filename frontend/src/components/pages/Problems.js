import React, { Component } from 'react';

import Navigation from '../Navigation';
import Footer from '../Footer';
import UtilityBar from '../UtilityBar';

export default class Problems extends Component {
    componentDidMount() {
        document.title = "Problems - Online Grader";
    }

    render() {
        return (
            <div>
                <div className="content">
                    <Navigation />

                    <div className="container py-3 mb-0">
                        <h3 className="my-0 font-italic">
                            Problems
                        </h3>
                    </div>

                    <UtilityBar />
                </div>

                <Footer />
            </div>

        );
    }
}