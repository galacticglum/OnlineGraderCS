import React, { Component } from 'react'
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom'; 
import PropTypes from 'prop-types';

export default function(ComposedComponent) {
    class Authenticate extends Component {
        componentWillMount() {
            const { isAuthenticated } = this.props.authentication;
            if (!isAuthenticated) {
                this.props.history.replace('/login', { referrer: this.props.location });
            }
        }

        componentWillUpdate(nextProps) {
            const { isAuthenticated } = nextProps.authentication;
            if (!isAuthenticated) {
                this.props.history.replace('/');
            }
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

