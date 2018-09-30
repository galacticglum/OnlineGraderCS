import axios from 'axios';

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