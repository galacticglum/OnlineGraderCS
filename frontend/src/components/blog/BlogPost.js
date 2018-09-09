import React from 'react';
import { Row, Col } from 'reactstrap';

import './BlogPost.css';

export default (props) => {
    return (
        <div className="blog-post">
            <h2 className="blog-post-title">{props.post.title}</h2>
            <p className="blog-post-meta">{props.post.date} by <a href="#">{props.post.user}</a></p>

            {props.post.content}
        </div>
    );
}