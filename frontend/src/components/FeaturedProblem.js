import React from 'react';
import FeaturedCard from './FeaturedCard';
import TagList from './TagList';

export default (props) => {
    const subtitle = ( <TagList className="mb-1" tags={props.problem.tags} /> );
    const link = {
        text: 'Solve problem'
    }

    return (
        <FeaturedCard section={props.problem.sortCategory} title={props.problem.title} 
            subtitle={subtitle} content={props.problem.description} link={link} />
    );
}