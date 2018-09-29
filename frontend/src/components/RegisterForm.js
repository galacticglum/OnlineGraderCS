import React, { Component } from 'react';
import PropTypes from 'prop-types';
import {
    Button,
    Form,
    FormGroup,
    Label,
    Input,
    FormText
} from 'reactstrap';

class RegisterForm extends Component {
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            email: '',
            password: '',
            passwordConfirmation: ''
        }

        this.onChange = this.onChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
    }

    onChange(e) {
        this.setState({ [e.target.name]: e.target.value });
    }

    onSubmit(e) {
        e.preventDefault();
        this.props.userSignupRequest(this.state);
    }

    render() {
        return (
            <Form onSubmit={this.onSubmit}>
                <FormGroup>
                    <Label for="usernameInput">Username</Label>
                    <Input type="text" name="username" id="usernameInput"
                        value={this.state.username} onChange={this.onChange} />
                </FormGroup>
                <FormGroup>
                    <Label for="emailInput">Email</Label>
                    <Input type="email" name="email" id="emailInput"
                        value={this.state.email} onChange={this.onChange} />
                </FormGroup>
                <FormGroup>
                    <Label for="passwordInput">Password</Label>
                    <Input type="password" name="password" id="passwordInput"
                        value={this.state.password} onChange={this.onChange} />
                </FormGroup>
                <FormGroup>
                    <Label for="confirmPasswordInput">Confirm Password</Label>
                    <Input type="password" name="passwordConfirmation" id="confirmPasswordInput"
                        value={this.state.passwordConfirmation} onChange={this.onChange} />
                </FormGroup>
                <FormGroup>
                    <Button color="primary">
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