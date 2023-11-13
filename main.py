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
python_out_file_path = f"{out_folder}/{file_name}.py"
json_ld_out_file_path = f"{out_folder}/{file_name}.jsonld"
json_out_file_path = f"{out_folder}/{file_name}.json"

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


def add_classes(base: str, classes: str, out_file: str, folder: str = "tmp"):
    yaml = ruamel.yaml.YAML()
    with open(f"{folder}/{base}") as fp:
        base_yaml = yaml.load(fp)
    with open(f"{folder}/{classes}") as fp:
        class_yaml = yaml.load(fp)
    base_yaml["classes"] = class_yaml
    with open(f"{out_file}", "w") as outfile:
        yaml.dump(base_yaml, outfile)


add_classes("meta.yaml", "classes.yaml", schema_out_file_path)


# Work around a bug in the original schema generator https://github.com/linkml/linkml/issues/1567
class CustomOwlSchemaGenerator(OwlSchemaGenerator):
    def end_schema(self, output=None, **_) -> None:
        data = self.graph.serialize(
            format="turtle" if self.format in ["owl", "ttl"] else self.format
        )
        print(output)
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

python = PythonGenerator(schema_out_file_path)
code = python.serialize(directory_output=True)
write_file(python_out_file_path, code)

schemas = JsonSchemaGenerator(
    schema_out_file_path, include_range_class_descendants=True
)
schema = schemas.serialize()
write_file(json_out_file_path, schema)

contextld = ContextGenerator(schema=schema_out_file_path)
contextld_content = contextld.serialize()
write_file(json_ld_out_file_path, contextld_content)
