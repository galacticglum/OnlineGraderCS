import React, { Component } from 'react';
import { Tooltip } from 'reactstrap';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faBars, faTable } from '@fortawesome/free-solid-svg-icons'

import './UtilityBar.css';

export default class UtilityBar extends Component {
    constructor(props) {
        super(props);

        this.cardViewTooltipToggle = this.cardViewTooltipToggle.bind(this);
        this.tableViewTooltipToggle = this.tableViewTooltipToggle.bind(this);
        this.state = {
            cardViewTooltipOpen: false,
            tableViewTooltipOpen: false
        }
    }

    cardViewTooltipToggle() {
        this.setState({
            cardViewTooltipOpen: !this.state.cardViewTooltipOpen
        });
    } 

    tableViewTooltipToggle() {
        this.setState({
            tableViewTooltipOpen: !this.state.tableViewTooltipOpen
        });
    }

    render() {
        return (
            <div className="container px-0 pb-4">
                <div className="bg-white border-bottom border-top">
                    <div className="d-flex flex-row">
                        <div className="d-flex flex-row utility-bar align-items-center my-2 px-4 border-right">
                            <span className="header-text smallcaps">View</span>
                            <button className="btn btn-sm view-button mr-1 py-0 my-0" id="card-view-btn">
                                <FontAwesomeIcon icon={faBars} id="card-view-btn-icon" />         
                            </button>
                            <Tooltip id="card-view-btn-icon" placement="top" isOpen={this.state.cardViewTooltipOpen} 
                                target="card-view-btn"  toggle={this.cardViewTooltipToggle} delay={{show: 1500, hide: 0}}>

                                Card View
                            </Tooltip>

                            <button className="btn btn-sm view-button mr-1 py-0 my-0" id="table-view-btn">
                                <FontAwesomeIcon icon={faTable} id="table-view-btn-icon" />         
                            </button>
                            <Tooltip id="table-view-btn-icon" placement="top" isOpen={this.state.tableViewTooltipOpen} 
                                target="table-view-btn" toggle={this.tableViewTooltipToggle} delay={{show: 1500, hide: 0}}>

                                Table View
                            </Tooltip>
                        </div>
                    </div>
                </div>
            </div>
        );
    }
}