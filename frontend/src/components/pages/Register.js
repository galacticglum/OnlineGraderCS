import React, { Component } from 'react';
import { connect } from 'react-redux';
import { userSignupRequest } from '../../actions/signupActions';

import PropTypes from 'prop-types';
import { Link } from 'react-router-dom'

import RegisterForm from '../RegisterForm';
import Navigation from '../Navigation';
import Footer from '../Footer';

class Register extends Component {
    componentDidMount() {
        document.title = "Register - Online Grader";
    }

    render() {
        const { userSignupRequest } = this.props;
        return (
            <div>
                <div className="content">
                    <Navigation />

                    <div className="container py-3 mb-0">
                        <h3 className="my-0">
                            Register
                        </h3>

                        <RegisterForm userSignupRequest={userSignupRequest} />
                        <p>Already signed up? Please <Link to="/login">login</Link>.</p>
                    </div>
                </div>

                <Footer />
            </div>
        )
    }
}

Register.propTypes = {
    userSignupRequest: PropTypes.func.isRequired
}

export default connect(null, { userSignupRequest })(Register);