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


# Test Case 3 - Grault 
GRAULT_PROTO = """
syntax = "proto3";
package tc3;
message Grault {
    string id = 1;
}
"""

grault_data = {
    "schema": GRAULT_PROTO,
    "schemaType": "PROTOBUF",
}

# Test Case 3 - Waldo 
WALDO_PROTO = """
syntax = "proto3";
package tc3;
message Waldo {
    string id = 1;
}
"""

waldo_data = {
    "schema": WALDO_PROTO,
    "schemaType": "PROTOBUF",
}

# Test Case 3 - Grault Updated
GRAULT_UPDATED_PROTO = """
syntax = "proto3";
package tc3;
import waldo.proto;
message Grault {
    string id = 1;
    Waldo child = 2;
}
"""

grault_updated_data = {
    "schema": GRAULT_UPDATED_PROTO,
    "schemaType": "PROTOBUF",
    "references": [{
        "name": "waldo.proto",
        "subject": "waldo",
        "version": -1,
    }]
}



logging.debug(">>>> Registering grault proto")
register("grault", grault_data)

logging.debug(">>>> Registering waldo proto")
register("waldo", waldo_data)

set_compatibility("grault", "FULL_TRANSITIVE")
set_compatibility("waldo", "FULL_TRANSITIVE")

logging.debug(">>>> Registering grault updated proto")
register("grault", grault_updated_data)

