import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Link } from 'react-router-dom'
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
    DropdownItem,
    Button
} from 'reactstrap';

import { connect } from 'react-redux';
import { userLogout } from '../actions/authenticationActions';

import './Navigation.css';

class Navigation extends Component {
    constructor(props) {
        super(props);

        this.toggle = this.toggle.bind(this);
        this.logout = this.logout.bind(this);

        this.state = {
            isOpen: false
        }
    }

    toggle() {
        this.setState({
            isOpen: !this.state.isOpen
        });
    }

    logout(e) {
        e.preventDefault();
        this.props.userLogout();
    }

    render() {
        const navLineClass = this.props.includeLine === true ? 'nav-line' : '';
        const { isAuthenticated, user } = this.props.authentication;

        return (
            <div className={'container px-0'}>
                <Navbar light expand="md" className={"justify-content-center py-3 nav-header " + navLineClass}>
                    <NavbarBrand tag={Link} to="/" className="d-flex w-50 mr-auto text-dark nav-header-brand">
                        <strong>
                            SLS
                            <span style={{ letterSpacing: '6px' }}>
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
                                <NavLink tag={Link} to="/problems">Problems</NavLink>
                            </NavItem>
                            <NavItem>
                                <NavLink tag={Link} to="/contests">Contests</NavLink>
                            </NavItem>
                            <NavItem>
                                <NavLink tag={Link} to="/ranks">Ranks</NavLink>
                            </NavItem>
                            <NavItem>
                                <NavLink tag={Link} to="/about">About</NavLink>
                            </NavItem>
                        </Nav>

                        <Nav className="ml-auto w-100 justify-content-end align-items-center" navbar>
                            <NavItem>
                                <NavLink className="text-muted" tag={Link} to="/search">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"
                                        strokeLinecap="round" strokeLinejoin="round">
                                        <circle cx="10.5" cy="10.5" r="7.5"></circle>
                                        <line x1="21" y1="21" x2="15.8" y2="15.8"></line>
                                    </svg>
                                </NavLink>
                            </NavItem>

                            {isAuthenticated ?
                                <UncontrolledDropdown nav inNavbar>
                                    <DropdownToggle caret nav>
                                        {user.identity.username}{' '}
                                    </DropdownToggle>

                                    <DropdownMenu>
                                    <DropdownItem tag={Link} to="/profile">Profile</DropdownItem>
                                        <DropdownItem tag={Link} to="/settings">Settings</DropdownItem>

                                        <DropdownItem divider />

                                        <DropdownItem onClick={this.logout}>Logout</DropdownItem>
                                    </DropdownMenu>
                                </UncontrolledDropdown>
                                :
                                <NavItem>
                                    <Link to="/login">
                                        <Button outline color="secondary" size="sm">
                                            Sign in
                                    </Button>
                                    </Link>
                                </NavItem>
                            }
                        </Nav>
                    </Collapse>
                </Navbar>

                <div className={this.props.childrenClassName}>
                    {this.props.children}
                </div>
            </div>
        );
    }
}

Navigation.propTypes = {
    authentication: PropTypes.object.isRequired,
    userLogout: PropTypes.func.isRequired
}

Navigation.defaultProps = {
    includeLine: true,
    childrenClassName: 'px-3'
}

function mapStateToProps(state) {
    return {
        authentication: state.authentication
    }
}

export default connect(mapStateToProps, { userLogout })(Navigation);