import React, { Component } from 'react'
import { Breadcrumb, BreadcrumbItem } from 'reactstrap';

import Navigation from './Navigation';
import './BreadcrumbNavigation.css';

export default class BreadcrumbNavigation extends Component {
    render() {
        return (
            <Navigation childrenClassName='px-0' includeLine={false}>
                <Breadcrumb listClassName="breadcrumb-nav my-0 mx-0" className="my-0 py-0">
                    {this.props.children}
                </Breadcrumb>
            </Navigation>
        )
    }
}
