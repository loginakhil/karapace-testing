import json
import requests
import logging

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)


KARAPACE_URL = "http://localhost:8080"

def get_versions(subject):
    response = requests.get(f"{KARAPACE_URL}/subjects/{subject}/versions")
    return response.json()

def get_all_schema_info():
    schema_infos = ""
    response = requests.get(f"{KARAPACE_URL}/subjects")
    if response.ok:
        for subject in response.json():
            schema_infos += f"Schema: {subject}, version: {get_versions(subject)} \n"
    else:
        logging.error(f"Error fetching schema {response.text}")
    return schema_infos

def register(subject, data):
    response = requests.post(
        f"{KARAPACE_URL}/subjects/{subject}/versions",
        headers={'Content-Type': 'application/vnd.schemaregistry.v1+json'},
        data=json.dumps(data))
    if response.ok:
        logging.debug(f"Schema ({subject}) registered successfully! {response.text}")
    else:
        logging.error(f"Error registering schema: {subject}, {response.text}")

def set_compatibility(subject, compatibility_type):
    url = f"{KARAPACE_URL}/config/{subject}"
    data = {"compatibility": compatibility_type}
    response = requests.put(url, headers={'Content-Type': 'application/json'}, data=json.dumps(data))
    if response.ok:
        logging.debug(f"Compatibility for {subject} set to {compatibility_type}")
    else:
        logging.error(f"Error setting compatibility for {subject}: {response.text}")


# Test Case 8 - Foo
FOO_PROTO = """
syntax = "proto3";
package tc1;
message Foo {
    string id = 1;
}
"""

foo_data = {
    "schema": FOO_PROTO,
    "schemaType": "PROTOBUF",
}

# Test Case 8 - Bar
BAR_PROTO = """
syntax = "proto3";
package tc1;
message Bar {
    string id = 1;
}
"""

bar_data = {
    "schema": BAR_PROTO,
    "schemaType": "PROTOBUF",
}

# Test Case 8 - Baz
BAZ_PROTO = """
syntax = "proto3";
package tc1;
import "foo.proto";
import "bar.proto";

message Baz {
    Foo foo = 1;
    Bar bar = 2;
}
"""

baz_data = {
    "schema": BAZ_PROTO,
    "schemaType": "PROTOBUF",
    "references": [{
        "name": "foo.proto",
        "subject": "foo",
        "version": -1,
    },{
        "name": "bar.proto",
        "subject": "bar",
        "version": -1,
    }]
}

# Test Case 8 - Baz_modified
BAZ_MODIFIED_PROTO = """
syntax = "proto3";
package tc1;
import "foo.proto";
import "bar.proto";

message Baz {
    Foo foo = 1;
    Bar bar = 2;
    string foobar = 3;
}
"""

baz_modified_data = {
    "schema": BAZ_MODIFIED_PROTO,
    "schemaType": "PROTOBUF",
    "references": [{
        "name": "foo.proto",
        "subject": "foo",
        "version": -1,
    },{
        "name": "bar.proto",
        "subject": "bar",
        "version": -1,
    }]
}

# Test Case 8 - Foo modified
FOO_MODIFIED_PROTO = """
syntax = "proto3";
package tc1;
message Foo {
    string id = 1;
    string name = 2;
}
"""

foo_modified_data = {
    "schema": FOO_MODIFIED_PROTO,
    "schemaType": "PROTOBUF",
}

################# First registration
logging.info(">>>> Registering foo proto")
register("foo", foo_data)
logging.info(">>>> Registering bar proto")
register("bar", bar_data)
logging.info(">>>> Registering baz proto")
register("baz", baz_data)

logging.info("Schema version information before re-upload")
logging.info("\n"+get_all_schema_info())

################# Re-registration
logging.info(">>>> Registering foo proto")
register("foo", foo_data)
logging.info(">>>> Registering bar proto")
register("bar", bar_data)
logging.info(">>>> Registering baz proto")
register("baz", baz_data)

logging.info("Schema version information after re-upload")
logging.info("\n"+get_all_schema_info())

################# Modification of the referencing proto

logging.info(">>>> Registering foo proto")
register("foo", foo_data)
logging.info(">>>> Registering bar proto")
register("bar", bar_data)
logging.info(">>>> Registering baz proto")
register("baz", baz_modified_data)

logging.info("Schema version information after modification of the referencing proto")
logging.info("\n"+get_all_schema_info())

################# Modification of the referenced proto

logging.info(">>>> Registering foo proto")
register("foo", foo_modified_data)
logging.info(">>>> Registering bar proto")
register("bar", bar_data)
logging.info(">>>> Registering baz proto")
register("baz", baz_modified_data)

logging.info("Schema version information after modification of the referenced proto")
logging.info("\n"+get_all_schema_info())
