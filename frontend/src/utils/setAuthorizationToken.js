import axios from 'axios';

export default function setAuthorizationToken(accessToken) {
    if (accessToken) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${accessToken}`;
    } else {
        delete axios.defaults.headers.common['Authorization'];
    }
}