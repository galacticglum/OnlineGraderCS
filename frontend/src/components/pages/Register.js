import React, { Component } from 'react'
import { 
    Button, 
    Form, 
    FormGroup,
    Label,
    Input,
    FormText } from 'reactstrap';

import { Link } from 'react-router-dom'
import axios from 'axios';

import Navigation from '../Navigation';
import Footer from '../Footer';

export default class Register extends Component {
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
    

    componentDidMount() {
        document.title = "Register - Online Grader";
    }

    onChange(e) {
        this.setState({ [e.target.name]: e.target.value});
    }

    onSubmit(e) {
        e.preventDefault();
        axios.post('http://localhost:5000/api/users/register', { 
            header: {
                'Content-Type': 'application/json'
            },
            username: this.state.username,
            email: this.state.email,
            password: this.state.password
        });
    }

    render() {
        return (
            <div>
                <div className="content">
                    <Navigation />

                    <div className="container py-3 mb-0">
                        <h3 className="my-0">
                            Register
                        </h3>

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
                        <p>Already signed up? Please <Link to="/login">login</Link>.</p>
                    </div>
                </div>

                <Footer />
            </div>
        )
    }
}
