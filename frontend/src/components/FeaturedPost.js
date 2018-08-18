import React from 'react';
import { Jumbotron, Col } from 'reactstrap';
import Truncate from 'react-truncate';

export default (props) => {
    return ( 
        <Jumbotron className="p-3 p-md-5 text-white rounded bg-dark mt-3">
            <Col md="6" className="px-0">
                <h1 className="display-4 font-italic py-1">
                    <Truncate lines={2}>
                        {props.post.title}
                    </Truncate>
                </h1>
                <p className="lead my-3">
                    <Truncate lines={3}>
                        {props.post.content}
                    </Truncate>
                </p>
                <p className="lead mb-0">
                    <a href="#" className="text-white font-weight-bold">Continue reading...</a>
                </p>
            </Col>
        </Jumbotron>
    );
}