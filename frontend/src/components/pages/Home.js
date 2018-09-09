import React, { Component } from 'react';
import { Row, Col } from 'reactstrap';

import Navigation from '../Navigation';
import FeaturedPost from '../FeaturedPost';
import FeaturedProblem from '../FeaturedProblem';
import FeaturedContest from '../FeaturedContest';
import Footer from '../Footer';

import Blog from '../blog/Blog';
import BlogSidebar from '../blog/BlogSidebar';

export default class App extends Component {
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
        },
        posts: [
            {
                title: 'Sample blog post',
                date: 'January 1, 2014',
                user: 'Mark',
                content: (
                    <div>

                        <p>This blog post shows a few different types of content that's supported and styled with Bootstrap.
                            Basic typography, images, and code are all supported.</p>
                        <hr />
                        <p>Cum sociis natoque penatibus et magnis
                            <a href="#">dis parturient montes</a>, nascetur ridiculus mus. Aenean eu leo quam. Pellentesque ornare sem
              lacinia quam venenatis vestibulum. Sed posuere consectetur est at lobortis. Cras mattis consectetur
                            purus sit amet fermentum.</p>
                        <blockquote>
                            <p>Curabitur blandit tempus porttitor.
                                <strong>Nullam quis risus eget urna mollis</strong> ornare vel eu leo. Nullam id dolor id nibh ultricies
                                vehicula ut id elit.</p>
                        </blockquote>
                        <p>Etiam porta
                            <em>sem malesuada magna</em> mollis euismod. Cras mattis consectetur purus sit amet fermentum. Aenean
                            lacinia bibendum nulla sed consectetur.</p>
                        <h2>Heading</h2>
                        <p>Vivamus sagittis lacus vel augue laoreet rutrum faucibus dolor auctor. Duis mollis, est non commodo
                            luctus, nisi erat porttitor ligula, eget lacinia odio sem nec elit. Morbi leo risus, porta ac
                            consectetur ac, vestibulum at eros.</p>
                        <h3>Sub-heading</h3>
                        <p>Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.</p>
                        <pre><code>Example code block</code></pre>
                        <p>Aenean lacinia bibendum nulla sed consectetur. Etiam porta sem malesuada magna mollis euismod. Fusce
                            dapibus, tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa.</p>
                        <h3>Sub-heading</h3>
                        <p>Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Aenean lacinia
                            bibendum nulla sed consectetur. Etiam porta sem malesuada magna mollis euismod. Fusce dapibus,
                            tellus ac cursus commodo, tortor mauris condimentum nibh, ut fermentum massa justo sit amet risus.</p>
                        <ul>
                            <li>Praesent commodo cursus magna, vel scelerisque nisl consectetur et.</li>
                            <li>Donec id elit non mi porta gravida at eget metus.</li>
                            <li>Nulla vitae elit libero, a pharetra augue.</li>
                        </ul>
                        <p>Donec ullamcorper nulla non metus auctor fringilla. Nulla vitae elit libero, a pharetra augue.</p>
                        <ol>
                            <li>Vestibulum id ligula porta felis euismod semper.</li>
                            <li>Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus.</li>
                            <li>Maecenas sed diam eget risus varius blandit sit amet non magna.</li>
                        </ol>
                        <p>Cras mattis consectetur purus sit amet fermentum. Sed posuere consectetur est at lobortis.</p>
                    </div>

                )
            }
        ]
    }

    componentDidMount() {
        document.title = "Home - Online Grader";
    }

    render() {
        return (
            <div>
                <div className="content">
                    <Navigation>
                        <FeaturedPost post={{
                            title: 'Title of a longer featured blog blog blog blog post',
                            content: `Multiple lines of text that form the lede, informing new readers quickly and efficiently about what\'s most interesting in this post\'s contents.`
                        }} />

                        <Row>
                            <FeaturedProblem problem={this.state.problem} />
                            <FeaturedContest contest={this.state.contest} />
                        </Row>
                    </Navigation>

                    <main role="main" className="container">
                        <Row>
                            <Col md="8" className="blog-main">
                                <Blog posts={this.state.posts} />
                            </Col>

                            <BlogSidebar />
                        </Row>
                    </main>
                </div>

                <Footer />
            </div>

        );
    }
}