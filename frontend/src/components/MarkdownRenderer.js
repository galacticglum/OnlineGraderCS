import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import markdown from 'markdown-it';
import mathjax from 'markdown-it-mathjax';

export default class MarkdownRenderer extends Component {
    constructor(props) {
        super(props);
        this.markdown = markdown().use(mathjax());
        this.state = {markdownData: ''};
    }

    setMarkdown = (markdown) => {
        this.setState({markdownData: markdown});
    }

    renderMathJax = () => {
        if (!window.MathJax || !window.MathJax.Hub) return;

        const currentNode = ReactDOM.findDOMNode(this);
        window.MathJax.Hub.Queue(['Typeset', window.MathJax.Hub, currentNode]);
    }

    componentWillMount() {
        if(this.props.src) {
            fetch(this.props.src)
            .then(res => {
                if(!res.ok) {
                    return 'Error: Markdown not found!';
                } else {
                    return res.text();
                }
            }).then(markdownData => this.setMarkdown(markdownData));
        } else if(this.props.text) {
            this.setMarkdown(this.props.text);
        }
    }

    componentDidMount() {
        this.renderMathJax();
    }
    
    componentDidUpdate() {
        this.renderMathJax();
    }

    render() {
        const markdown = this.markdown.render(this.state.markdownData);
        return (
            <div className={this.props.className} dangerouslySetInnerHTML={{__html:markdown}} />
        );
    }
}
