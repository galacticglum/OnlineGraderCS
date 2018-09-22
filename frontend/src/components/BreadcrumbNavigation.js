import React, { Component } from 'react'
import { Breadcrumb, BreadcrumbItem } from 'reactstrap';

import Navigation from './Navigation';
import './BreadcrumbNavigation.css';

export default class BreadcrumbNavigation extends Component {
    render() {
        return (
            <Navigation includeLine={false}>
                <Breadcrumb listClassName="breadcrumb-nav my-0 mx-0" className="my-0 py-0">
                    <BreadcrumbItem><a href="#">Home</a></BreadcrumbItem>
                    <BreadcrumbItem><a href="#">Library</a></BreadcrumbItem>
                    <BreadcrumbItem active>Data</BreadcrumbItem>
                </Breadcrumb>
            </Navigation>
        )
    }
}
