import React, { Component } from 'react'
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom'; 
import PropTypes from 'prop-types';

export default function(ComposedComponent) {
    class Authenticate extends Component {
        checkAuthentication(isAuthenticated, redirectUrl='/login') {
            if (!isAuthenticated) {
                this.props.history.replace(redirectUrl);
            }
        }

        componentWillMount() {
            const { isAuthenticated } = this.props.authentication;
            this.checkAuthentication(isAuthenticated);
        }

        componentWillUpdate(nextProps) {
            const { isAuthenticated } = nextProps.authentication;
            this.checkAuthentication(isAuthenticated, '/');
        }

        render() {
            const { isAuthenticated } = this.props.authentication;
            if (!isAuthenticated) return null;   

            return (
                <ComposedComponent  {...this.props} />
            )
        }
    }

    function mapStateToProps(state) {
        return {
            authentication: state.authentication
        }
    }

    Authenticate.propTypes = {
        authentication: PropTypes.object.isRequired,
        history: PropTypes.object.isRequired
    }

    return withRouter(connect(mapStateToProps)(Authenticate));
}

