import React, { Component } from 'react';
import NewsPost from './NewsPost';

export default class News extends Component {
    render() {
        const postElements = this.props.posts.map((post, i) =>
            <div key={i}>
                <NewsPost post={post} />
            </div>
        );

        return (
            <div>
                <h3 className="pb-3 mb-4 mt-2 font-italic border-bottom">
                    {this.props.headerTitle}
                </h3>

                {postElements}
            </div>
        );
    }
}

News.defaultProps = {
    headerTitle: "News"
}