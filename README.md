# formify-cli

> A CLI tool that generates accessible HTML forms from JSON schema definitions with built-in validation.

---

## Installation

```bash
pip install formify-cli
```

Or install from source:

```bash
git clone https://github.com/yourusername/formify-cli.git
cd formify-cli
pip install .
```

---

## Usage

Define your form structure in a JSON schema file:

```json
{
  "title": "Contact Form",
  "fields": [
    { "name": "email", "type": "email", "required": true, "label": "Email Address" },
    { "name": "message", "type": "textarea", "required": true, "label": "Your Message" }
  ]
}
```

Then run the CLI to generate your HTML form:

```bash
formify generate schema.json --output form.html
```

Additional options:

```bash
formify generate schema.json --theme minimal --validate
formify validate schema.json        # Validate schema without generating
formify --help                      # Show all available commands
```

The generated `form.html` will include semantic HTML5 markup, ARIA attributes, and client-side validation based on your schema constraints.

---

## Features

- ✅ Accessible HTML5 output with ARIA support
- ✅ Built-in client-side validation
- ✅ Multiple themes (`default`, `minimal`, `bootstrap`)
- ✅ Schema validation before generation

---

## License

This project is licensed under the [MIT License](LICENSE).