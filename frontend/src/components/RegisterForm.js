import React, { Component } from 'react';
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

    onSubmit(e) {
        e.preventDefault();

        this.setState({ isLoading: true });
        this.props.userSignupRequest(this.state)
            .then(() => {})
            .catch((res) => {
                this.setState({errors: res.response.data, isLoading: false})
            });
    }

    render() {
        const { errors } = this.state;

        return (
            <Form onSubmit={this.onSubmit}>
                <FormGroup>
                    <Label for="usernameInput">Username</Label>
                    <Input type="text" name="username" id="usernameInput"
                        value={this.state.username} onChange={this.onChange} 
                        invalid={(errors.parameter_info && errors.parameter_info.username) && true} />

                    {(errors.parameter_info && errors.parameter_info.username) && 
                        <FormFeedback>{errors.parameter_info.username}</FormFeedback>}
                </FormGroup>
                <FormGroup>
                    <Label for="emailInput">Email</Label>
                    <Input type="email" name="email" id="emailInput"
                        value={this.state.email} onChange={this.onChange}
                        invalid={(errors.parameter_info && errors.parameter_info.email) && true} />
                        
                    {(errors.parameter_info && errors.parameter_info.email) && 
                        <FormFeedback>{errors.parameter_info.email}</FormFeedback>}
                </FormGroup>
                <FormGroup>
                    <Label for="passwordInput">Password</Label>
                    <Input type="password" name="password" id="passwordInput"
                        value={this.state.password} onChange={this.onChange}
                        invalid={(errors.parameter_info && errors.parameter_info.password) && true} />

                    {(errors.parameter_info && errors.parameter_info.password) && 
                        <FormFeedback>{errors.parameter_info.password}</FormFeedback>}
                </FormGroup>
                <FormGroup>
                    <Label for="confirmPasswordInput">Confirm Password</Label>
                    <Input type="password" name="passwordConfirmation" id="confirmPasswordInput"
                        value={this.state.passwordConfirmation} onChange={this.onChange} />
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

export default RegisterForm;