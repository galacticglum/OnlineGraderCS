import React from 'react';
import FeaturedCard from './FeaturedCard';
import TagList from './TagList';

export default (props) => {
    const section = {
        name: 'Featured Contest',
        className: 'text-success'
    }

    const subtitle = (
        <div className="mb-1 text-muted">
            <i>{props.contest.start}{' '}-{' '}{props.contest.end}</i>
        </div>
    );

    const link = {
        text: 'Join contest'
    }

    return (
        <FeaturedCard section={section} title={props.contest.title} subtitle={subtitle} 
            content={props.contest.description} link={link} thumbnail={props.contest.thumbnail} />
    );
}