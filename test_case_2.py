import requests
import json
import requests
import logging
import http.client


http.client.HTTPConnection.debuglevel = 1

logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)
requests_log = logging.getLogger("requests.packages.urllib3")
requests_log.setLevel(logging.DEBUG)
requests_log.propagate = True


KARAPACE_URL = "http://localhost:8080"


def get_all():
    response = requests.get(f"{KARAPACE_URL}/subjects")
    if response.ok:
        logging.debug(f"Schemas fetched successfully! {response.text}")
    else:
        logging.error(f"Error fetching schema {response.text}")

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


# Test Case 1 - Foo
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

# Test Case 1 - Bar 
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

# Test Case 1 - Baz 
BAZ_PROTO = """
syntax = "proto3";
package tc1;
import "foo.proto";

message Baz {
  oneof event_type {
    Foo foo = 1;
  }
}
"""

baz_data = {
    "schema": BAZ_PROTO,
    "schemaType": "PROTOBUF",
    "references": [{
        "name": "foo.proto",
        "subject": "foo",
        "version": -1,
    }]
}

# Test Case 1 - Baz Updated 
BAZ_UPDATED = """
syntax = "proto3";
package tc1;
import "foo.proto";
import "bar.proto";

message Baz {
  oneof event_type {
    Foo foo = 1;
    Bar bar = 2;
  }
}
"""

baz_updated_data = {
    "schema": BAZ_UPDATED,
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


logging.debug(">>>> Registering foo proto")
register("foo", foo_data)

logging.debug(">>>> Registering bar proto")
register("bar", bar_data)

logging.debug(">>>> Registering baz proto")
register("baz", baz_data)

set_compatibility("foo", "FULL_TRANSITIVE")
set_compatibility("bar", "FULL_TRANSITIVE")
set_compatibility("baz", "FULL_TRANSITIVE")

logging.debug(">>>> Registering baz updated proto")
register("baz", baz_updated_data)

