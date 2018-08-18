import React, { Component } from 'react';
import { Row } from 'reactstrap';

import Navigation from './components/Navigation';
import FeaturedProblem from './components/FeaturedProblem';
import FeaturedContest from './components/FeaturedContest';

class App extends Component {
  state = {
    problem: {
      title: 'Sherlock and Array',
      description: 'Watson gives Sherlock an array of integers. His challenge is to find an element of the array such that the sum of all elements to the left is equal to the sum of all elements to the right. For instance, given the array [5,6,8,11],8 is between two subarray that sum to 11.',
      tags: [
        {
          name: 'algorithms',
          className: 'badge-danger'
        },
        {
          name: 'graphs',
          className: 'badge-warning'
        },
        {
          name: 'maths',
          className: 'badge-info'
        }
      ],
      sortCategory: {
        name: 'Trending',
        className: 'text-primary'
      }
    },
    contest: {
      title: 'Summer Contest #2',
      description: 'This is a wider card with supporting text below as a natural lead-in to additional content.',
      start: 'Jul 24, 2018, 00:00',
      end: 'Jul 30, 2018, 00:00',
      thumbnail: {
        source: 'https://i.imgur.com/hGxZnur.png',
        alt: 'Card image caption'
      }
    }
  }

  render() {
    return (
      <div className="content">
        <Navigation>
          <Row>
            <FeaturedProblem problem={this.state.problem} />
            <FeaturedContest contest={this.state.contest} />
          </Row>
        </Navigation>
      </div>
    );
  }
}

export default App;
