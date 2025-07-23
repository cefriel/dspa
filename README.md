# DSPA - Dataspace vocabulary

A metadata schema to represent Data Product Offerings in dataspaces, aligned with Open Data Product Specifications (v3.1), DCAT-AP and EDC metadata schema.

| Prefix    | IRI |
| -- | ------- |
| dspa:  | [https://knowledge.c-innovationhub.com/dspa#](https://knowledge.c-innovationhub.com/dspa#)  |

## Main concept
The main idea is to convert the metadata model of [Open Data Product Specifications](https://opendataproducts.org/v3.1) into an ontology and adapt it to link to a DCAT metadata model and to Eclipse Dataspace Connector policies model.
The resulting model is roughly [this](./draft-ontology.png).

### `widoco`: RDF to HTML
Download release JAR from [here](https://github.com/dgarijo/Widoco/releases) and rename it as `widoco.jar`. Documentation for the CLI tool is available [here](https://github.com/dgarijo/Widoco#how-to-use-widoco). The `run-onto.sh` script was tested with version `1.4.21`.

3. Execute the `sh run-onto.sh my-ontology x.y.z` script providing as argument the correct version number.

4. Edit the documentation in the [sections](.dspa/sections) folder

5. Git commit and push

6. Enable GitHub Pages to host the ontology

7. Configure a webserver by using the provided [.htaccess](.dspa/.htaccess) file.


