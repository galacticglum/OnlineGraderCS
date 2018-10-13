import axios from 'axios';

export function getProblemData(problemId) {
    return dispatch => {
        return axios.get('http://localhost:5000/api/problem/' + problemId);
    }
}