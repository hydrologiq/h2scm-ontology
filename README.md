## Local Setup

To run these scripts locally you need to install python using pyenv and the following pip requirements. You can do this by following the commands below.

1. `eval "$(pyenv init -)"`
1. `pyenv install` (optional)
1. `pyenv exec python -m venv .venv`
1. `source .venv/bin/activate`
1. `pip3 install -r requirements.txt` (optional)

## Ontology

- namespace: `hydrogen_nrmm`

### Instance creation

- `id` -- `hydrogen_nrmm:<uuid4>`

### Known issues

- Specifying an array of objects produces a key error, meaning a URI or CURIE (the `id`) will need to be referenced. This means any objects will need to be created as instances of the class.
