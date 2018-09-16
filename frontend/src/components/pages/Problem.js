import React, { Component } from 'react'
import { withRouter } from 'react-router-dom'; 

class Problem extends Component {
    componentWillMount() {
        const { id } = this.props.match.params;

        if (isNaN(parseInt(id))) {
            this.props.history.replace('/404');
        }
    }

    render() {
        const { id } = this.props.match.params;

        return (
            <div>
                {id}
            </div>
        )
    }
}

export default withRouter(Problem);