import React from 'react';

export default (props) => {
    const tagElements = props.tags.map((tag, i) =>
        <span key={i} >
            <a href="#" className={"badge badge-pill " + tag.className}>{tag.name}</a>{' '}
        </span>
    );

    return (
        <div className={props.className}>
            {tagElements}
        </div>
    );
}