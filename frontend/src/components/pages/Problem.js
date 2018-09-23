import React, { Component } from 'react'
import { 
    Row, 
    Col, 
    BreadcrumbItem,
    Button,
    Badge,
    Table } from 'reactstrap';

import { withRouter } from 'react-router-dom'; 

import BreadcrumbNavigation from '../BreadcrumbNavigation';
import Footer from '../Footer';
import TagList from '../TagList';

import './Problem.css';

class Problem extends Component {
    state = {
        tags: [
            {
                name: 'algorithms',
                className: 'badge-danger'
            },
            {
                name: 'graphs',
                className: 'badge-warning'
            },
            {
                name: 'maths',
                className: 'badge-info'
            },
            {
                name: 'xyz',
                className: 'badge-dark'
            },
            {
                name: 'abc',
                className: 'badge-info'
            }
        ]
    }

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
                    <BreadcrumbNavigation>
                        <BreadcrumbItem><a href="#">Problems</a></BreadcrumbItem>
                        <BreadcrumbItem><a href="#">CCC</a></BreadcrumbItem>
                        <BreadcrumbItem active>CCC '15 S2 - Jerseys</BreadcrumbItem>
                    </BreadcrumbNavigation>

                    <div className="container py-3">
                        <Col md="12" className="px-0">
                            <h2 className="problem-title">CCC '15 S2 - Jerseys</h2>     
                            {/* <div className="d-flex flex-row"> 
                                <h2 className="problem-title">CCC '15 S2 - Jerseys</h2>
                                <Badge className="ml-auto align-self-end" color="success">Easy</Badge>
                            </div> */}
                            <hr/>
                        </Col>

                        <Row className="px-0">
                            <Col md="9">
                                <div className="problem-description">
                                    <p><strong>Canadian Computing Competition: 2015 Stage 1, Senior #2</strong></p>
                                    <p>
                                        A school team is trying to assign jerseys numbered 1, 2, 3, ..., J to student athletes. The size of
                                        jersey is either small (<code>S</code>), medium (<code>M</code>), or large (<code>L</code>).
                                    </p>

                                    <p>
                                        Each athlete has requested a specific jersey number and a preferred size. The athletes will not be satisfied with
                                        a jersey that is the wrong number or that is smaller than their preferred size. They will be satisfied with a 
                                        jersey that is their preferred size or larger as long as it is the right number. Two students cannot be given the
                                        same jersey number.
                                    </p>

                                    <p>
                                        Your task is to determine the maximum number of requests that can be satisfied.
                                    </p>
                                </div>
           
                                <div className="py-1 problem-constraints">
                                    <h5>Constraints</h5>
                                    <hr className="mt-0" />
                                    <p>
                                        1 ≤ j ≤ J
                                    </p>
                                    <p>
                                        1 ≤ a ≤ A
                                    </p>
                                </div>

                                <div className="py-1 problem-input-spec">
                                    <h5>Input Specification</h5>
                                    <hr className="mt-0" />
                                    <p>
                                        The first line of input is the integer J which is the number of jerseys.
                                    </p>
                                    <p>
                                        The second line of input is the integer A which is the number of athletes.
                                    </p>
                                    <p>
                                        The next J lines are each the character <code>S</code>, <code>M</code>, or <code>L</code>. Line j gives the
                                        size of the jersey j.
                                    </p>
                                    <p>
                                        The last A lines are each the character <code>S</code>, <code>M</code>, or <code>L</code> followed by a space, followed
                                        by an integer. Line a gives the requested size and jersey number for athlete a where the athletes are numbered 
                                        1, 2, 3, ..., A.
                                    </p>
                                    <p>
                                        For 50% of the test cases, 1 ≤ J ≤ 10^3  and 1 ≤ A ≤ 10^3.
                                    </p>
                                    <p>
                                        For the remaining 50% of the test cases, 1 ≤ J ≤ 10^6  and 1 ≤ A ≤ 10^6.
                                    </p>
                                </div>

                                <div className="py-1 problem-output-spec">
                                    <h5>Output Specification</h5>
                                    <hr className="mt-0" />
                                    <p>
                                        One day you woke up, finding yourself back in 1992. 
                                        It would seem that the gypsy wife of the wizened old monk 
                                        whose voodoo shop you smash up every day after school has cast a spell on you.
                                    </p>
                                </div>

                            </Col>
                            <Col md="3" className="order-first order-md-2">
                                {/* <p className="blog-post-meta">{props.post.date} by <a href="#">{props.post.user}</a></p> */}
                                
                                <Button color="info" className="mb-0 btn-submit-solution">
                                    Submit Solution
                                </Button>
                                <hr className="my-2" />
                                <Table className="m-0" borderless={true}>
                                    <tbody>
                                    <tr>
                                        <th scope="row" className="m-0 p-0 text-muted">Difficulty</th>
                                        <td className="m-0 p-0 text-right"><Badge color="success">Easy</Badge></td>
                                    </tr>
                                    </tbody>
                                </Table>
                                <hr className="my-2" />
                                <div>
                                    <a href="#" className="muted-link">All Submissions</a>
                                </div>
                                <div>
                                    <a href="#" className="muted-link">Best Submissions</a>
                                </div>
                                <hr className="my-2" />
                                <div className="text-muted">
                                    Tags
                                </div>
                                <TagList tags={this.state.tags} />
                            </Col>
                        </Row>

                    </div>
                </div>

                <Footer />
            </div>
        )
    }
}

export default withRouter(Problem);