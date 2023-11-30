## Ontology

This is where the ontology concerning the management of the Hydrogen Non-road mobile machinery (NRMM) supply chain. The ontology follows the [OWL standard](https://www.w3.org/OWL/) and is defined using [LinkML](https://linkml.io/linkml/) in [YAML](https://yaml.org/).

### Namespace

The namespace that the ontology follows is `https://w3id.org/hydrologiq/hydrogen/nrmm` which is prefixed as `hydrogen_nrmm`.

### Making changes

1. All changes should be made on a branch and a PR created following the template
   - Branches should be appropriately named e.g. `relationship-changes`
   - Commits should be made using gitmoji see the [development guide](https://coda.io/d/_d36dB83GZVM/Development_suNC1#_luVgb)
1. The PR does not need a reviewer but if you think it needs one please request it
1. Merge the PR
1. Delete the branch (can be done via UI or cli with `git branch -D <branch_name>`)

### Release process

1. Tag a commit with a version e.g. `git tag -a v1.3.0 -m "Tagging v1.3.0 release"`
1. Push that tag `git push origin v1.3.0`
1. Create a release within GitHub

   1. Navigate to this [repository]()
   1. On the right hand navigation click on the `Releases` section

   <img src="./docs/imgs/create_release_1.png" alt="Navigate to releases" height="300"/>

   3. Once on releases click on `Tags`
   1. Once on tags click on the `...` menu for the tag you previously

   <img src="./docs/imgs/create_release_2.png" alt="Navigate to tags" width="500"/>

   5. Click on `Create release`

   <img src="./docs/imgs/create_release_3.png" alt="Release description" height="400"/>

   6. For the title just put the release version and the text release e.g. `v1.3.0 release`
   1. Then for the description put a bullet point list of what has changed
   1. For the attachment you need to upload the bundled version of the ontology, this needs to be the `ontology.zip` artifact of the bundle related to the commit you have tagged for this release
   1. Ensure that `Set as the latest release` is selected
   1. Click `Publish release` 🥳

#### Post release

1. Ensure that any repositories which are using the ontology are updated to the latest release, currently this is done by updating the `pre-build.sh` script in every relevant repository.

### Instance details

- `id` -- `hydrogen_nrmm:<uuid4>`

### Known issues

- Specifying an array of objects produces a key error, meaning a URI or CURIE (the `id`) will need to be referenced. This means any objects will need to be created as instances of the class.

## Local Setup

To run these scripts locally you need to install python using pyenv and the following pip requirements. You can do this by following the commands below.

1. `eval "$(pyenv init -)"`
1. `pyenv install` (optional)
1. `pyenv exec python -m venv .venv`
1. `source .venv/bin/activate`
1. `pip3 install -r requirements.txt` (optional)
