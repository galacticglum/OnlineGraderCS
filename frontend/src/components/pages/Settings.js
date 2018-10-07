import React, { Component } from 'react'
import requireAuth from '../../utils/requireAuthentication';

import Navigation from '../Navigation';
import Footer from '../Footer';

class Settings extends Component {
    componentDidMount() {
        document.title = "Settings - Online Grader";
    }

    render() {
        return (
            <div>
                <div className="content">
                    <Navigation />

                    <div className="container py-3 mb-0">
                        <h3>Settings</h3>
                        <h1>{this.props.authentication.user.identity.username}</h1>
                    </div>
                </div>

                <Footer />
            </div>
        )
    }
}

export default requireAuth(Settings);
