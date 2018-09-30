import React, { Component } from 'react';
import { withRouter } from 'react-router-dom'; 

import PropTypes from 'prop-types';
import {
    Button,
    Form,
    FormGroup,
    Label,
    Input,
    FormFeedback
} from 'reactstrap';

import validateInput from '../validations/signup';
import FormTextField from './FormTextField';

class RegisterForm extends Component {
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            email: '',
            password: '',
            passwordConfirmation: '',
            errors: {},
            isLoading: false,
            invalid: false
        }

        this.onChange = this.onChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
        this.checkUserExists = this.checkUserExists.bind(this);
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

        if (this.isValid()) {
            this.setState({ isLoading: true });
            this.props.userSignupRequest(this.state)
                .then(() => {
                    this.props.history.push('/login');
                })
                .catch((res) => {
                    this.setState({errors: res.response.data.parameter_info, isLoading: false})
                });
        }
    }

    checkUserExists(e) {
        const field = e.target.name;
        const value = e.target.value;
        
        this.props.userExists({[field]: value}).then(res => {
            let errors = this.state.errors;
            errors[field] = 'This ' + field + ' is already taken!';
            this.setState({errors: errors, invalid: true});

        }).catch(res => {
            let errors = this.state.errors;
            errors[field] = null;
            this.setState({errors: errors, invalid: false});
        });    
    }

    render() {
        const { errors } = this.state;

        return (
            <Form onSubmit={this.onSubmit}>
                <FormTextField field="username" value={this.state.username}
                    label="Username" error={errors.username}
                    type="text" onChange={this.onChange}
                    checkUserExists={this.checkUserExists}
                />

                <FormTextField field="email" value={this.state.email}
                    label="Email" error={errors.email}
                    type="text" onChange={this.onChange}
                    checkUserExists={this.checkUserExists}
                />

                <FormTextField field="password" value={this.state.password}
                    label="Password" error={errors.password}
                    type="password" onChange={this.onChange} />

                <FormTextField field="passwordConfirmation" value={this.state.passwordConfirmation}
                    label="Confirm Password" error={errors.passwordConfirmation}
                    type="password" onChange={this.onChange} />

                <FormGroup>
                    <Button color="primary" disabled={this.state.isLoading || this.state.invalid}>
                        Sign up
                    </Button>
                </FormGroup>
            </Form>
        )
    }
}

RegisterForm.propTypes = {
    userSignupRequest: PropTypes.func.isRequired,
    userExists: PropTypes.func.isRequired
}

export default withRouter(RegisterForm);