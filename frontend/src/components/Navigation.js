import React from 'react';
import { NavLink } from 'react-router-dom';
import NavigationLink from './NavigationLink';

const navigation = (props) => {
    return (
        <div className="container">
            <nav className="navbar navbar-light navbar-expand-md bg-faded 
                justify-content-center blog-header py-3 px-0">

                {/* Navbar brand */}
                <NavLink to="/" className="navbar-brand d-flex w-50 mr-auto blog-header-logo text-dark">
                    <strong>SLS<span style={{letterSpacing: 6 + 'px'}}>S<span className="text-primary">::</span></span>OJ</strong>
                </NavLink>

                <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbar">
                    <span className="navbar-toggler-icon"></span>
                </button>

                <div className="navbar-collapse collapse w-100" id="navbar">
                    <ul className="navbar-nav w-100 justify-content-center">
                        <NavigationLink exact={true} strict to="/problems" className="nav-item" activeClassName="active">
                            <span className="nav-link text-muted">Problems</span>
                        </NavigationLink>
                        <NavigationLink exact={true} strict to="/contests" className="nav-item" activeClassName="active">
                            <span className="nav-link text-muted">Contests</span>
                        </NavigationLink>
                        <NavigationLink exact={true} strict to="/ranks" className="nav-item" activeClassName="active">
                            <span className="nav-link text-muted">Ranks</span>
                        </NavigationLink>
                        <NavigationLink exact={true} strict to="/about" className="nav-item" activeClassName="active">
                            <span className="nav-link text-muted">About</span>
                        </NavigationLink>
                    </ul>

                    <ul className="nav navbar-nav ml-auto w-100 justify-content-end align-items-center">
                        <a className="text-muted" href="#">
                            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"
                                strokeLinecap="round" strokeLinejoin="round" className="mx-3">
                                <circle cx="10.5" cy="10.5" r="7.5"></circle>
                                <line x1="21" y1="21" x2="15.8" y2="15.8"></line>
                            </svg>
                        </a>

                        <li className="nav-item dropdown">
                            <a className="nav-link dropdown-toggle" href="#" id="user_dropdown" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                <i className="fas fa-user"></i>
                                <span className="mx-1" >Shon Verch</span>
                                <span className="caret"></span>
                            </a>
                            <div className="dropdown-menu" aria-labelledby="user_dropdown">
                                <a className="dropdown-item" href="{{ url_for('settings') }}">Settings</a>
                                <a className="dropdown-item" href="{{ url_for('security.logout') }}">Log out</a>
                            </div>
                        </li>
                    </ul>
                </div>
            </nav>
        </div>
    )
}

export default navigation;