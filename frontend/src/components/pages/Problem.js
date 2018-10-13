import React, { Component } from 'react'
import { 
    Row, 
    Col, 
    BreadcrumbItem,
    Button,
    Badge,
    Table,
    Collapse } from 'reactstrap';

import PropTypes from 'prop-types';
import { Link, withRouter } from 'react-router-dom'; 
import { connect } from 'react-redux';
import { getProblemData } from '../../actions/problemActions';

import BreadcrumbNavigation from '../BreadcrumbNavigation';
import Footer from '../Footer';
import TagList from '../TagList';
import CollapseLabel from '../CollapseLabel';
import MarkdownRenderer from '../MarkdownRenderer';

import './Problem.css';

class DividerLine extends Component {
    render(props) {
        return (
            <div>
                <h5>{this.props.children}</h5>
                <hr className="mt-0" />
            </div>
        );
    }
}

class Problem extends Component {
    constructor(props) {
        super(props);
        this.state = {
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
    }
    

    componentDidMount() {
        const { id } = this.props.match.params;

        this.props.getProblemData(id)
            .then(res => this.setState({problemData: res.data}))
            .catch(error => this.props.history.replace('/404'));
    }

    render() {
        // Don't render the component
        // unless there is an actual problem
        // to render.
        if (!this.state.problemData) {
            return null;
        }

        let constraintsSection = null;
        if (this.state.problemData.problem.constraints) {
            constraintsSection = (        
                <div className="pt-3 problem-constraints">
                    <DividerLine>Constraints</DividerLine>
                    <MarkdownRenderer text={this.state.problemData.problem.constraints} />
                </div>
            );
        }

        let inputSpecSection = null;
        if (this.state.problemData.problem.input_spec) {
            inputSpecSection = (
                <div className="pt-3 problem-input-spec">
                    <DividerLine>Input Specification</DividerLine>
                    <MarkdownRenderer text={this.state.problemData.problem.input_spec} />
                </div>
            );
        }

        let outputSpecSection = null;
        if (this.state.problemData.problem.output_spec) {
            outputSpecSection = (
                <div className="pt-3 problem-output-spec">
                    <DividerLine>Output Specification</DividerLine>
                    <MarkdownRenderer text={this.state.problemData.problem.output_spec} />
                </div>
            );
        }
        
        return (
            <div>
                <div className="content">
                    <BreadcrumbNavigation>
                        <BreadcrumbItem><a href="#">Problems</a></BreadcrumbItem>
                        <BreadcrumbItem><a href="#">CCC</a></BreadcrumbItem>
                        <BreadcrumbItem active>{this.state.problemData.problem.title}</BreadcrumbItem>
                    </BreadcrumbNavigation>

                    <div className="container py-3">
                        <Col md="12" className="px-0">
                            <h2 className="problem-title">{this.state.problemData.problem.title}</h2>     
                            <hr/>
                        </Col>
                        <Row className="px-0">
                            <Col md="9">
                                <div className="problem-description">
                                    <MarkdownRenderer text={this.state.problemData.problem.description} />
                                </div>

                                {constraintsSection}
                                {inputSpecSection}
                                {outputSpecSection}       
                            </Col>
                            <Col md="3" className="order-first order-md-2">    
                                <Link to={this.props.match.params.id + '/submit'}>
                                    <Button color="info" className="mb-0 btn-submit-solution">
                                        Submit Solution
                                    </Button>
                                </Link>
                                <hr className="my-2" />
                                <Table className="m-0" borderless={true}>
                                    <tbody>
                                    <tr>
                                        <th scope="row" className="m-0 p-0 text-muted">Difficulty</th>
                                        <td className="m-0 p-0 text-right"><Badge color="success">Easy</Badge></td>
                                    </tr>
                                    <tr>
                                        <th scope="row" className="m-0 p-0 text-muted">Points</th>
                                        <td className="m-0 p-0 text-right">{this.state.problemData.problem.points}</td>
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
                                <CollapseLabel isOpen={true} labelClassName="text-muted font-weight-bold" labelText="Tags">
                                    <TagList className="ml-3" tags={this.state.tags} />
                                </CollapseLabel>
                            </Col>
                        </Row>

                    </div>
                </div>

                <Footer />
            </div>
        )
    }
}

Problem.propTypes = {
    getProblemData: PropTypes.func.isRequired
}

export default connect(null, { getProblemData })(withRouter(Problem));