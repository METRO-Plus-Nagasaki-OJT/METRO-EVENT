# Clover Validation Plugin Documentation

## Overview

Clover is a JavaScript validation library designed to work seamlessly with Alpine.js. It provides various validation rules and can be easily integrated into forms to validate user input.

## Using Clover Validation Without Alpine.js (not stable)

If you're not using Alpine.js and want to validate form data using Clover, you can directly call the validation functions in your script.

### Example Script

```html
<body>
    <form id="myForm">
        <label for="name">Name:</label>
        <input
            id="name"
            name="name"
            type="text"
        />
        <br />

        <!-- Other form fields here -->

        <button
            type="button"
            onclick="validateForm()"
        >
            Validate
        </button>
    </form>

    <script>
        // Define validation rules
        const rule = {
            name: [
                Clover.rule.required('Name is required'),
                Clover.rule.number('Name must be a number'),
                Clover.rule.password(
                    'Name must contain at least one letter and one number'
                ),
            ],
        };

        // Function to validate form
        function validateForm() {
            // Get form data
            const formData = new FormData(document.getElementById('myForm'));
            let data = {};
            for (var [key, value] of formData.entries()) {
                data[key] = value;
            }
            // Validate form data
            const errors = Clover.validate({ data, rule });
            // Display errors or proceed with form submission
            if (Object.keys(errors).length === 0) {
                alert('Form is valid! Proceed with submission.');
            } else {
                alert('Form validation failed! Please check the errors.');
            }
        }
    </script>
</body>
```

## Using Clover Validation with Alpine.js

### Form Setup

Create a form and use the x-clover-form directive to attach Clover validation to it. Use the x-clover-verify directive on input fields to specify validation rules.

```html
<body>
    <form
        x-data="form"
        x-clover-form="submit"
    >
        <input
            name="name"
            type="text"
            x-clover-verify
        />
        <div x-text="errors.name"></div>
        <button type="submit">Submit</button>
    </form>
    <script>
        document.addEventListener('alpine:init', function () {
            window.Alpine.data('form', () => ({
                rule: {
                    name: [
                        Clover.rule.required(),
                        Clover.rule.number(),
                        Clover.rule.password(),
                    ],
                },
                errors: {},
                submit() {
                    // Your form submission logic here
                },
            }));
        });
    </script>
</body>
```

## Validation Rules

Clover provides several built-in validation rules which can be applied to form fields:

-   required(message): Ensures the field is not empty.
-   mail(message): Validates the field against an email format.
-   password(message): Validates the field to contain at least - one letter and one number.
-   string(message): Ensures the field is a string.
-   enum({ list }, message): Validates the field to match one of the - values in the provided list.
-   number(message): Ensures the field contains only numbers.
-   custom(message, callback): Allows for custom validation logic.
-   sameWith({ name: ["confirmPassword"] }): Validates that the field's value matches the value of the confirmPassword field.
-   min({ target: "string", amount: 8 }): Validates that the string field has a minimum length of 8 characters.
-   max({ target: "number", amount: 100 }): Validates that the numeric field has a value less than or equal to 100.

### Example Usage

Here's a complete example integrating Clover with a simple HTML form:

```html
<body>
    <form
        x-data="form"
        x-clover-form="submit"
    >
        <label for="name">Name:</label>
        <input
            id="name"
            name="name"
            type="text"
            x-clover-verify
        />
        <div x-text="errors.name"></div>

        <label for="email">Email:</label>
        <input
            id="email"
            name="email"
            type="email"
            x-clover-verify
        />
        <div x-text="errors.email"></div>

        <label for="password">Password:</label>
        <input
            id="password"
            name="password"
            type="password"
            x-clover-verify
        />
        <div x-text="errors.password"></div>

        <button type="submit">Submit</button>
    </form>
    <script>
        document.addEventListener('alpine:init', function () {
            Alpine.data('form', () => ({
                rule: {
                    name: [
                        Clover.rule.required('Name is required'),
                        Clover.rule.onlyWordCharacter(),
                    ],
                    email: [
                        Clover.rule.required('Email is required'),
                        Clover.rule.mail('Invalid email format'),
                    ],
                    password: [
                        Clover.rule.required('Password is required'),
                        Clover.rule.password(),
                    ],
                },
                errors: {},
                submit() {
                    // Your form submission logic here
                },
            }));
        });
    </script>
</body>
```

## Notes

-   The **x-clover-verify** directive, used for real-time validation on input fields, is optional. If omitted, validation will occur only when the form is submitted.
-   Validation Messages: Custom validation messages can be provided to each rule for better user feedback.
-   Dynamic Form Data: Form data is automatically collected using new FormData(form), making it easy to handle submissions.

_Created by Wai Yan Lin for METRO OJT Project._
