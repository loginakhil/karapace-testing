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


# Test Case 2 - Qux 
QUX_PROTO = """
syntax = "proto3";
package tc2;
message Qux {
    string id = 1;
}
"""

qux_data = {
    "schema": QUX_PROTO,
    "schemaType": "PROTOBUF",
}

# Test Case 2 - Qux Updated
QUX_UPDATED_PROTO = """
syntax = "proto3";
package tc2;
message Qux {
    string id = 1;
    Corge child = 2;
}

message Corge {
    string id = 1;
}
"""

qux_updated_data = {
    "schema": QUX_UPDATED_PROTO,
    "schemaType": "PROTOBUF",
}



logging.debug(">>>> qux proto")
register("qux", qux_data)

set_compatibility("qux", "FULL_TRANSITIVE")

logging.debug(">>>> Registering qux updated proto")
register("qux", qux_updated_data)

