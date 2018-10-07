import React, { Component } from 'react';
import { withRouter } from 'react-router-dom'; 
import { connect } from 'react-redux';
import { userLoginRequest } from '../actions/authenticationActions';

import PropTypes from 'prop-types';
import {
    Button,
    Form,
    FormGroup,
    UncontrolledAlert 
} from 'reactstrap';

import FormTextField from './FormTextField';
import validateInput from '../validations/login';

class LoginForm extends Component {
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            password: '',
            errors: {},
            isLoading: false
        }

        this.onChange = this.onChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
    }
    
    
    onChange(e) {
        this.setState({ [e.target.name]: e.target.value });
    }

    isValid() {
        const { errors, isValid } = validateInput(this.state);
        if (!isValid) {
            this.setState({errors});
        }

        return isValid;
    }

    onSubmit(e) {
        e.preventDefault();
        if(this.isValid()) {
            this.setState({ isLoading: true });
            this.props.userLoginRequest(this.state.username, this.state.password)
                .then(() => {
                    if (this.props.location.state && this.props.location.state.referrer) {
                        this.props.history.push(this.props.location.state.referrer.pathname);
                    } else {
                        this.props.history.push('/');
                    }
                })
                .catch(res => {
                    let errors = this.state.errors;
                    errors['form'] = 'Invalid username or password!';
                    this.setState({errors: errors, isLoading: false});
                });
        }
    }

    render() {
        const { errors } = this.state;
        return (
            <Form onSubmit={this.onSubmit}>
                {errors.form && 
                    <UncontrolledAlert color="danger">{errors.form}</UncontrolledAlert >}

                <FormTextField field="username" value={this.state.username}
                    label="Username" error={errors.username}
                    type="text" onChange={this.onChange}
                />

                <FormTextField field="password" value={this.state.password}
                    label="Password" error={errors.password}
                    type="password" onChange={this.onChange} />

                <FormGroup>
                    <Button color="primary" disabled={this.state.isLoading}>
                        Login
                    </Button>
                </FormGroup>
            </Form>
        )
    }
}

LoginForm.propTypes = {
    userLoginRequest: PropTypes.func.isRequired
}

export default connect(null, { userLoginRequest })(withRouter(LoginForm));