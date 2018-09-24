import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { Collapse } from 'reactstrap';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faChevronRight } from '@fortawesome/free-solid-svg-icons';

import './CollapseLabel.css';

class CollapseLabel extends Component {
    state = {
        collapse: this.props.isOpen
    }
    
    toggle = () => {
        this.setState({collapse: !this.state.collapse});
    }

    render() {
        const collapseStateClass = this.state.collapse ? 'collapsed' : '';

        return (
            <div>
                <div className={'collapse-label ' + this.props.labelClassName} onClick={this.toggle}>
                    <FontAwesomeIcon className={this.props.faIconClassName + ' collapse-icon mr-1 ' + collapseStateClass} 
                        icon={this.props.faIcon} /> {this.props.labelText}
                </div>
                <Collapse isOpen={this.state.collapse}>
                    {this.props.children}
                </Collapse>
            </div>
        )
    }
}

CollapseLabel.propTypes = {
    faIcon: PropTypes.object,
    faIconClassName: PropTypes.string,
    labelClassName: PropTypes.string,
    labelText: PropTypes.string.isRequired,
    isOpen: PropTypes.bool
}

CollapseLabel.defaultProps = {
    faIcon: faChevronRight,
    isOpen: false
}

export default CollapseLabel;

