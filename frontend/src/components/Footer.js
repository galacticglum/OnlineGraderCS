import React from 'react';
import './Footer.css';

export default (props) => {
    return (
        <footer>
            <div className="container" id="footer">
                <div className="text-center">
                    <ul className="list-inline my-2">
                        <li className="list-inline-item">
                            <a href="about.html">About</a>
                        </li>
                        <li className="list-inline-item">
                            <a href="privacy.html">Privacy</a>
                        </li>
                        <li className="list-inline-item">
                            <a href="terms.html">Terms</a>
                        </li>
                    </ul>

                    <p className="my-1" id="powered-by">
                        Powered by{' '}
                        <a href="http://flask.pocoo.org/">
                            <strong>Flask</strong>
                        </a>{' '}and{' '}
                        <a href="https://www.python.org/">
                            <strong>Python 3.6</strong>
                        </a>
                    </p>
                </div>
            </div>

            <p class="text-center text-muted" id="footer-text">
                &copy; 2018{' '}
                <a href="https://galacticglum.com/">Shon Verch</a> and <a href="#">contributors</a>
            </p>
        </footer>
    );
}