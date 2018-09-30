import React, { Component } from 'react';

import PropTypes from 'prop-types';
import { Link } from 'react-router-dom'

import LoginForm from '../LoginForm';
import Navigation from '../Navigation';
import Footer from '../Footer';

class Login extends Component {
    componentDidMount() {
        document.title = "Login - Online Grader";
    }

    render() {
        return (
            <div>
                <div className="content">
                    <Navigation />

                    <div className="container py-3 mb-0">
                        <h3 className="my-0">
                            Login
                        </h3>

                        <LoginForm />
                        <p>Not yet signed up? Please <Link to="/register">register for an account</Link>.</p>
                    </div>
                </div>

                <Footer />
            </div>
        )
    }
}

export default Login;