import React, { Component } from 'react'
import { Breadcrumb, BreadcrumbItem } from 'reactstrap';
import { withRouter } from 'react-router-dom'; 

import BreadcrumbNavigation from '../BreadcrumbNavigation';
import Footer from '../Footer';

import './Problem.css';

class Problem extends Component {
    componentWillMount() {
        const { id } = this.props.match.params;

        let intId = parseInt(id);
        if(intId != parseFloat(id) || intId <= 0) {
            this.props.history.replace('/404');
        }
    }

    render() {
        const { id } = this.props.match.params;

        return (
            <div>
                <div className="content">
                    <BreadcrumbNavigation />

                    <div className="container py-3">
                        <h2 className="problem-title">16 BIT S/W ONLY</h2>
                        <hr/>
                        {/* <p className="blog-post-meta">{props.post.date} by <a href="#">{props.post.user}</a></p> */}

                        <p>
                            One day you woke up, finding yourself back in 1992. 
                            It would seem that the gypsy wife of the wizened old monk 
                            whose voodoo shop you smash up every day after school has cast a spell on you.
                        </p>
                    </div>
                </div>

                <Footer />
            </div>
        )
    }
}

export default withRouter(Problem);