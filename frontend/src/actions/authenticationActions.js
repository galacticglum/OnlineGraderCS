import axios from 'axios';
import jwt from 'jsonwebtoken';

import setAuthorizationToken from '../utils/setAuthorizationToken';
import { SET_CURRENT_USER } from './types';

export function userSignupRequest(userData) {
    return dispatch => {
        return axios.post('http://localhost:5000/api/users/register', {
            ...userData,
            headers: {
                'Content-Type': 'application/json'
            }
        });
    }
}

export function userExists(userData) {
    return dispatch => {
        return axios.post('http://localhost:5000/api/users/find', {
            ...userData,
            headers: {
                'Content-Type': 'application/json'
            }
        });
    }
}

export function userLoginRequest(username, password) {
    return dispatch => {
        return axios.get('http://localhost:5000/api/users/authenticate', {
            auth: {
                username: username,
                password: password
            }
        }).then(res => {
            const access_token = res.data.access_token;
            const refresh_token = res.data.refresh_token;

            localStorage.setItem('access_token', access_token);
            localStorage.setItem('refresh_token', refresh_token);

            setAuthorizationToken(access_token);
            dispatch(setCurrentUser(jwt.decode(access_token)));
        });
    }
}

export function setCurrentUser(user) {
    return {
        type: SET_CURRENT_USER,
        user
    }
}