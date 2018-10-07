import axios from 'axios';
import store from '../store';
import { setCurrentUser } from '../actions/authenticationActions';
import jwt from 'jsonwebtoken';

export default function setAuthorizationToken(accessToken) {
    if (accessToken) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;
        store.dispatch(setCurrentUser(jwt.decode(accessToken)));
    } else {
        delete axios.defaults.headers.common['Authorization'];
    }
}