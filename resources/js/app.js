import Alpine from 'alpinejs'

window.Alpine = Alpine

const Clover = {
    rule: {
        required: function (message) {
            return function (field, val) {
                return {
                    rule: 'required',
                    value: val ? false : message || `The ${field} is required`,
                };
            };
        },
        mail: function (message) {
            return function (field, val) {
                const regex =
                    /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
                return {
                    rule: 'mail',
                    value: val.match(regex)
                        ? false
                        : message ||
                        `The  ${field}  does not match with mail format`,
                };
            };
        },
        password: function (message) {
            return function (field, val) {
                const regex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]$/;
                return {
                    rule: 'password',
                    value: val.match(regex)
                        ? false
                        : message ||
                        `The ${field} must have a minimum of eight characters with at least one alphabet and one number`,
                };
            };
        },
        string: function (message) {
            return function (field, val) {
                if (typeof val !== 'string') {
                    return {
                        rule: 'string',
                        value:
                            message ||
                            `The ${field} must be minimun minLength characters`,
                    };
                }
                return { value: false };
            };
        },
        enum: function (message) {
            return function (list) {
                return function (field, val) {
                    return {
                        rule: 'enum',
                        value: list.includes(val)
                            ? false
                            : message ||
                            `The ${field} must be include in ${list.join(
                                ','
                            )}`,
                    };
                };
            };
        },
        number: function (message) {
            return function (field, val) {
                var regex = /^[0-9]$/;
                if (!val.match(regex)) {
                    return {
                        rule: 'number',
                        value: message || `The ${field} must be number`,
                    };
                }
                return { value: false };
            };
        },
        custom: function (message) {
            return function (cb) {
                return function (field, val) {
                    return { rule: 'custom', value: message || cb(field, val) };
                };
            };
        },
        object: function (attr) {
            return this.validate(attr);
        },
    },
    validate: function ({ rule, data }) {
        const errors = {};
        for (let k in rule) {
            for (let r of rule[k]) {
                var error = r(k, data[k]);
                if (error.value) {
                    errors[k] = error.value;
                    break;
                }
            }
        }
        return errors;
    },
    form: function ({ form, rule, messages = {}, verify = false }) {
        var data = Object.fromEntries(new FormData(form));
        var errors = this.validate({ rule, data, messages });
        if (verify) {
            for (var key in errors) {
                form.querySelector(`[clover-verify="error-${key}"]`).innerText =
                    errors[key];
            }
        }
        return {
            valid: Object.keys(errors).length ? false : true,
            data,
            errors,
        };
    },
};

document.addEventListener('alpine:init', () => {
    window.Alpine.directive(
        'clover',
        function (el, { value, modifiers, expression }, { cleanup, evaluate }) {
            let timeout;
            let handler = () => {
                const errors = evaluate('errors');
                if (timeout) {
                    clearTimeout(timeout);
                }
                timeout = setTimeout(function () {
                    let error;
                    for (let r of evaluate(expression)) {
                        const e = r(value, el.value);
                        if (e.value) {
                            error = e.value;
                            break;
                        }
                    }

                    if (error) {
                        errors[value] = error;
                    } else {
                        errors[value] = '';
                    }
                }, 300);
            };

            el.addEventListener('input', handler);

            cleanup(() => {
                el.removeEventListener('input', handler);
            });
        }
    );
});

window.Clover = Clover

Alpine.start()