import React from 'react';
import PropTypes from 'prop-types';
import {
    FormGroup,
    Label,
    Input,
    FormFeedback
} from 'reactstrap';

const FormTextField = (props) => {
    const inputId = props.field + 'Input';
    return (
        <FormGroup>
            <Label for={inputId}>{props.label}</Label>
            <Input type={props.type} name={props.field} id={inputId}
                value={props.value} onChange={props.onChange}
                onBlur={props.checkUserExists}
                invalid={props.error && true} />

            {props.error && 
                <FormFeedback>{props.error}</FormFeedback>}
        </FormGroup>
    )
}


FormTextField.propTypes = {
    field: PropTypes.string.isRequired,
    value: PropTypes.string.isRequired,
    label: PropTypes.string.isRequired,
    error: PropTypes.string,
    type: PropTypes.string.isRequired,
    onChange: PropTypes.func.isRequired,
    checkUserExists: PropTypes.func
}

FormTextField.defaultProps = {
    type: 'text'
}

export default FormTextField;