import React, { Component } from 'react';
import {
    Collapse,
    Navbar,
    NavbarToggler,
    NavbarBrand,
    Nav,
    NavItem,
    NavLink,
    UncontrolledDropdown,
    DropdownToggle,
    DropdownMenu,
    DropdownItem } from 'reactstrap';

import './Navigation.css';

export default class Navigation extends Component {
    constructor(props) {
        super(props);

        this.toggle = this.toggle.bind(this);
        this.state = {
            isOpen: false
        }
    }

    toggle() {
        this.setState({
            isOpen: !this.state.isOpen
        });
    }

    render() {
        return (
            <div className="container">
                <Navbar light expand="md" className="justify-content-center py-3 nav-header">
                    <NavbarBrand href="/" className="d-flex w-50 mr-auto text-dark nav-header-brand">
                        <strong>
                            SLS
                            <span style={{letterSpacing: '6px'}}>
                                S
                                <span className="text-primary">::</span>
                            </span>
                            OJ
                        </strong>
                    </NavbarBrand>

                    <NavbarToggler onClick={this.toggle} />
                    <Collapse isOpen={this.state.isOpen} className="w-100" navbar>
                        <Nav className="w-100 justify-content-center" navbar>
                            <NavItem>
                                <NavLink href="/problems">Problems</NavLink>
                            </NavItem>
                            <NavItem>
                                <NavLink href="/contests">Contests</NavLink>
                            </NavItem>
                            <NavItem>
                                <NavLink href="/ranks">Ranks</NavLink>
                            </NavItem>
                            <NavItem>
                                <NavLink href="/about">About</NavLink>
                            </NavItem>
                        </Nav>

                        <Nav className="ml-auto w-100 justify-content-end align-items-center" navbar>
                            <NavItem>
                                <NavLink className="text-muted" href="/search">
                                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"
                                    strokeLinecap="round" strokeLinejoin="round">
                                    <circle cx="10.5" cy="10.5" r="7.5"></circle>
                                    <line x1="21" y1="21" x2="15.8" y2="15.8"></line>
                                </svg>
                                </NavLink>
                            </NavItem>
                            <UncontrolledDropdown nav inNavbar>
                                <DropdownToggle caret nav>
                                Shon Verch{' '}
                                </DropdownToggle>

                                <DropdownMenu>
                                    <DropdownItem>
                                        Profile
                                    </DropdownItem>
                                    <DropdownItem>
                                        Settings
                                    </DropdownItem>

                                    <DropdownItem divider />

                                    <DropdownItem>
                                        Logout
                                    </DropdownItem>
                                </DropdownMenu>
                            </UncontrolledDropdown>
                        </Nav>
                    </Collapse>
                </Navbar>

                {this.props.children}
            </div>
        );
    }
}