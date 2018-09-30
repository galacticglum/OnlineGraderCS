import Validator from 'validator';
import isEmpty from 'lodash/isEmpty';

export default function validateInput(data) {
    let errors = {};

    if (isEmpty(data.username)) {
        errors.username = 'Please provide a username.';
    }

    if (isEmpty(data.password)) {
        errors.password = 'Please provide a password.';
    }

    return { errors, isValid: isEmpty(errors) }
}