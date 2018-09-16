import React, { Component } from 'react'
import { withRouter } from 'react-router-dom'; 

class Problem extends Component {
    componentWillMount() {
        const { id } = this.props.match.params;

        let intId = parseInt(id);
        if(intId != parseFloat(id) || intId <= 0) {
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