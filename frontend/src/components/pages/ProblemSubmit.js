import React, { Component } from 'react'
import { 
    Card, 
    CardText, 
    CardBody, 
    CardTitle, 
    CardSubtitle,
    Button,
    CardImg,
    CardHeader,
    CardFooter
} from 'reactstrap';

import PropTypes from 'prop-types';
import { Link, withRouter } from 'react-router-dom'; 
import { connect } from 'react-redux';
import { getProblemData } from '../../actions/problemActions';
import requireAuth from '../../utils/requireAuthentication';

import Navigation from '../Navigation';
import Footer from '../Footer';

class ProblemSubmit extends Component {
    constructor(props) {
        super(props);
        this.state = {}
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

        return (
            <div>
                <div className="content">
                    <Navigation />

                    <div className="container py-3 mb-0 px-0">
                        <h2 className="px-3">
                            Submit to <Link to={'/problem/' + this.props.match.params.id}>{this.state.problemData.problem.title}</Link>
                        </h2>
                        <hr className="mb-0" />
                    </div>
                    <div className="container pb-3 mb-0">
                        <Card>
                            {/* <CardHeader>Header</CardHeader> */}
                            <CardBody>
                            <CardTitle>Special Title Treatment</CardTitle>
                            <CardText>With supporting text below as a natural lead-in to additional content.</CardText>
                            <Button>Go somewhere</Button>
                            </CardBody>
                            <CardFooter>Footer</CardFooter>
                        </Card>
                    </div>
                </div>

                <Footer />
            </div>
        )
    }
}

ProblemSubmit.propTypes = {
    getProblemData: PropTypes.func.isRequired
}

export default connect(null, { getProblemData })(requireAuth(ProblemSubmit));
