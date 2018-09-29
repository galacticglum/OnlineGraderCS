import React, { Component } from 'react'
import { 
    Button, 
    Form, 
    FormGroup,
    Label,
    Input,
    FormText } from 'reactstrap';

import { Link } from 'react-router-dom'

import Navigation from '../Navigation';
import Footer from '../Footer';

export default class Login extends Component {
    constructor(props) {
        super(props);
        this.state = {
            username: '',
            password: '',
        }

        this.onChange = this.onChange.bind(this);
        this.onSubmit = this.onSubmit.bind(this);
    }
    

    componentDidMount() {
        document.title = "Login - Online Grader";
    }

    onChange(e) {
        this.setState({ [e.target.name]: e.target.value});
    }

    onSubmit(e) {
        e.preventDefault();
        console.log(this.state);
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

                        <Form onSubmit={this.onSubmit}>
                            <FormGroup>
                                <Label for="usernameInput">Username</Label>
                                <Input type="text" name="username" id="usernameInput" 
                                        value={this.state.username} onChange={this.onChange} />
                            </FormGroup>
                            <FormGroup>
                                <Label for="passwordInput">Password</Label>
                                <Input type="password" name="password" id="passwordInput" 
                                        value={this.state.password} onChange={this.onChange} />
                            </FormGroup>
                            <FormGroup>
                                <Button color="primary">
                                    Sign in
                                </Button>
                            </FormGroup>
                        </Form>
                        <p>Not yet signed up? Please <Link to="/register">register for an account</Link>.</p>
                    </div>
                </div>

                <Footer />
            </div>
        )
    }
}
