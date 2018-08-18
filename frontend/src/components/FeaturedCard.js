import React from 'react';
import { Col, Card, CardBody, CardText, CardImg } from 'reactstrap';
import Truncate from 'react-truncate';
import './FeaturedCard.css';

function Thumbnail (props) {
    if ('image' in props && props.image != null) {
        return (
            <CardImg src={props.image.source} alt={props.image.alt} 
                className="card-img-right featured-card-thumbnail flex-auto d-none d-lg-block" />
        );
    }

    return (null);
}

export default (props) => {
    return (
        <Col md="6" className="featured-card">
            <Card className="flex-md-row mb-4 shadow-sm h-md-250">
                <CardBody className="d-flex flex-column align-items-start">
                    <strong className={"d-inline-block mb-2 " + props.section.className}>{props.section.name}</strong>
                    <h3 className="d-inline-block mb-0 w-100">
                        <Truncate lines={1}>
                            {props.title}
                        </Truncate>
                    </h3>
                    {props.subtitle}
                    <CardText className="mb-auto w-100">
                        <Truncate lines={3}>
                            {props.content}
                        </Truncate>
                    </CardText>
                    <a href="#">{props.link.text}</a>
                </CardBody>
                <Thumbnail image={props.thumbnail} />
            </Card>
        </Col>
    );
}