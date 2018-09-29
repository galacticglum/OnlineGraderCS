import React, { Component } from 'react';
import { withRouter } from 'react-router-dom'; 

import PropTypes from 'prop-types';
import {
    Button,
    Form,
    FormGroup,
    Label,
    Input,
    FormText,
    FormFeedback
} from 'reactstrap';

import validateInput from '../validations/signup';

class RegisterForm extends Component {
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            email: '',
            password: '',
            passwordConfirmation: '',
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

    render() {
        const { errors } = this.state;

        return (
            <Form onSubmit={this.onSubmit}>
                <FormGroup>
                    <Label for="usernameInput">Username</Label>
                    <Input type="text" name="username" id="usernameInput"
                        value={this.state.username} onChange={this.onChange} 
                        invalid={errors.username && true} />

                    {errors.username && 
                        <FormFeedback>{errors.username}</FormFeedback>}
                </FormGroup>
                <FormGroup>
                    <Label for="emailInput">Email</Label>
                    <Input type="email" name="email" id="emailInput"
                        value={this.state.email} onChange={this.onChange}
                        invalid={errors.email && true} />
                        
                    {errors.email && 
                        <FormFeedback>{errors.email}</FormFeedback>}
                </FormGroup>
                <FormGroup>
                    <Label for="passwordInput">Password</Label>
                    <Input type="password" name="password" id="passwordInput"
                        value={this.state.password} onChange={this.onChange}
                        invalid={errors.password && true} />

                    {errors.password && 
                        <FormFeedback>{errors.password}</FormFeedback>}
                </FormGroup>
                <FormGroup>
                    <Label for="confirmPasswordInput">Confirm Password</Label>
                    <Input type="password" name="passwordConfirmation" id="confirmPasswordInput"
                        value={this.state.passwordConfirmation} onChange={this.onChange}
                        invalid={errors.passwordConfirmation && true} />
                    
                    {errors.passwordConfirmation && 
                        <FormFeedback>{errors.passwordConfirmation}</FormFeedback>}
                </FormGroup>
                <FormGroup>
                    <Button color="primary" disabled={this.state.isLoading}>
                        Sign up
                    </Button>
                </FormGroup>
            </Form>
        )
    }
}

RegisterForm.propTypes = {
    userSignupRequest: PropTypes.func.isRequired
}

export default withRouter(RegisterForm);