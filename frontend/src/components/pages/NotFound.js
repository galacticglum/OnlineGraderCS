import React, { Component } from 'react'

import Navigation from '../Navigation';
import Footer from '../Footer';
import './NotFound.css'

export default class NotFound extends Component {
    componentDidMount() {
        document.title = "Page Not Found - Online Grader";
    }

    render() {
        return (
            <div>
                <div className="content">
                    <Navigation>
                        <div className="pt-4 d-flex flex-column align-items-center justify-content-center main-404">
                            <img src="/404_img.png" alt="404" className="img-responsive image-404"/>
                            <h4 className="mt-3">Ruh-oh!</h4>
                            <p>the page you requested does not exist</p>
                        </div>
                    </Navigation>
                </div>

                <Footer />
            </div>
        )
    }
}
