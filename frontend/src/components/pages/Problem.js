import React, { Component } from 'react'

export default class Problem extends Component {
    render() {
        const { id } = this.props.match.params;

        return (
            <div>
                {id}
            </div>
        )
    }
}
