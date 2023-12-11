import json
from linkml.generators.pythongen import PythonGenerator
from linkml.generators.owlgen import OwlSchemaGenerator, MetadataProfile
from linkml.generators.jsonschemagen import JsonSchemaGenerator
from linkml.generators.jsonldcontextgen import ContextGenerator
import os
import shutil
import ruamel.yaml
import glob

out_folder = "dist"
file_name = "hydrogen_nrmm"

rdf_out_file_path = f"{out_folder}/{file_name}.rdf"

schema_out_file_path = f"{out_folder}/{file_name}.yaml"
schema_inlined_out_file_path = f"{out_folder}/{file_name}_inlined.yaml"
schema_optional_out_file_path = f"{out_folder}/{file_name}_optional.yaml"

python_out_file_path = f"{out_folder}/{file_name}.py"
python_optional_out_file_path = f"{out_folder}/{file_name}_optional.py"

json_ld_out_file_path = f"{out_folder}/{file_name}.jsonld"

json_out_file_path = f"{out_folder}/{file_name}.json"
json_relationships_out_file_path = f"{out_folder}/{file_name}_relationships.json"
json_inlined_out_file_path = f"{out_folder}/{file_name}_inlined.json"
json_optional_out_file_path = f"{out_folder}/{file_name}_optional.json"

try:
    os.mkdir("tmp")
    shutil.rmtree(out_folder, ignore_errors=True)
    os.mkdir(out_folder)
except:
    pass

meta = glob.glob("meta/*.yaml")

classes = glob.glob("classes/**/*.yaml", recursive=True)


def mergefiles(file_name: str, files: [str], folder: str = "tmp"):
    with open(f"{folder}/{file_name}", "w") as outfile:
        for file in files:
            with open(file) as infile:
                outfile.write(infile.read())
        outfile.write("\n")


mergefiles("meta.yaml", meta)
mergefiles("classes.yaml", classes)


def set_slots(slots: [object], values: dict = {}):
    for slot in slots:
        slot = slots[slot]
        for key in values.keys():
            if key in slot:
                slot[key] = values[key]


def add_classes(
    base: str,
    classes: str,
    out_file: str,
    inlined_slots: bool = False,
    not_required: bool = False,
    folder: str = "tmp",
):
    yaml = ruamel.yaml.YAML()
    with open(f"{folder}/{base}") as fp:
        base_yaml = yaml.load(fp)
    with open(f"{folder}/{classes}") as fp:
        class_yaml = yaml.load(fp)
    base_yaml["classes"] = class_yaml

    if inlined_slots:
        set_slots(base_yaml["slots"], {"inlined": True, "inlined_as_list": True})
    if not_required:
        set_slots(base_yaml["slots"], {"required": False})

    with open(f"{out_file}", "w") as outfile:
        yaml.dump(base_yaml, outfile)


add_classes("meta.yaml", "classes.yaml", schema_out_file_path)
add_classes("meta.yaml", "classes.yaml", schema_inlined_out_file_path, True)
add_classes(
    "meta.yaml", "classes.yaml", schema_optional_out_file_path, not_required=True
)


# Work around a bug in the original schema generator https://github.com/linkml/linkml/issues/1567
class CustomOwlSchemaGenerator(OwlSchemaGenerator):
    def end_schema(self, output=None, **_) -> None:
        data = self.graph.serialize(
            format="turtle" if self.format in ["owl", "ttl"] else self.format
        )
        if output:
            with open(output, "w", encoding="UTF-8") as outf:
                outf.write(data)
        else:
            print(data)


owl = CustomOwlSchemaGenerator(
    schema_out_file_path,
    metadata_profile=MetadataProfile.rdfs,
    type_objects=False,
    format="xml",
    metaclasses=False,
)


def write_file(name, content):
    with open(name, "w") as outfile:
        outfile.write(content)


rdf = owl.serialize()
rdf = rdf.replace("None", "").strip()
write_file(rdf_out_file_path, rdf)

shutil.rmtree("tmp", ignore_errors=True)


def generate_python(schema_file_path: str, out_python_file_path: str):
    python = PythonGenerator(schema_file_path)
    code = python.serialize(directory_output=True)
    write_file(out_python_file_path, code)


generate_python(schema_out_file_path, python_out_file_path)
generate_python(schema_optional_out_file_path, python_optional_out_file_path)


def generate_json_relationships(schema):
    class SetEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, set):
                return list(obj)
            return json.JSONEncoder.default(self, obj)

    def remove_ref(ref: str):
        return ref.replace("#/$defs/", "")

    relationships = {}
    for _, def_value in schema["$defs"].items():
        if "properties" in def_value:
            for prop, prop_value in def_value["properties"].items():
                classes = set({})
                arr = []
                if "anyOf" in prop_value:
                    arr = prop_value["anyOf"]
                if "items" in prop_value:
                    if "$ref" in prop_value["items"]:
                        arr = [prop_value["items"]]
                    elif "anyOf" in prop_value["items"]:
                        arr = prop_value["items"]["anyOf"]
                if "$ref" in prop_value:
                    arr = [prop_value]
                if len(arr) > 0:
                    for class_name in arr:
                        obj_name = remove_ref(class_name["$ref"])
                        if schema["$defs"][obj_name]["type"] == "object":
                            classes.add(obj_name)
                if len(classes) > 0:
                    if relationships.get(prop):
                        for class_name in classes:
                            relationships[prop].add(class_name)
                    else:
                        relationships[prop] = classes

    write_file(
        json_relationships_out_file_path, json.dumps(relationships, cls=SetEncoder)
    )


# Only generate a JSON Schema for inlined and non inlined
def generate_json(
    schema_file_path: str, out_file_path: str, generate_relationships: bool = False
):
    schemas = JsonSchemaGenerator(
        schema_file_path,
        include_range_class_descendants=True,
    )

    if generate_relationships:
        generate_json_relationships(schemas.generate())

    write_file(out_file_path, schemas.serialize())


generate_json(schema_out_file_path, json_out_file_path)
generate_json(schema_inlined_out_file_path, json_inlined_out_file_path, True)
generate_json(schema_optional_out_file_path, json_optional_out_file_path)


contextld = ContextGenerator(schema=schema_out_file_path)
contextld_content = contextld.serialize()
write_file(json_ld_out_file_path, contextld_content)
