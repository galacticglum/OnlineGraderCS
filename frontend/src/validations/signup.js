import Validator from 'validator';
import isEmpty from 'lodash/isEmpty';

export default function validateInput(data) {
    let errors = {};

    if (isEmpty(data.username)) {
        errors.username = 'Please choose a username.';
    }

    if (isEmpty(data.email)) {
        errors.email = 'Please provide an email address.';
    }
    else if(!Validator.isEmail(data.email)) {
        errors.email = 'Please provide a valid email address.';
    }

    if(!Validator.equals(data.password, data.passwordConfirmation)) {
        errors.passwordConfirmation = 'Ruh-oh! The passwords do not match!';
    }

    if (isEmpty(data.password) || !Validator.isLength(data.password, 6)) {
        errors.password = 'Please choose a password that is at least 6 character long.';
    }

    if (isEmpty(data.passwordConfirmation)) {
        errors.passwordConfirmation = 'Please confirm your password.';
    }

    return { errors, isValid: isEmpty(errors) }
}