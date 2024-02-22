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


# Test Case 10
V1_PROTO = """
syntax = "proto3";

package message;
option go_package = "./message/v1;message";

message EnvelopeV1 {
  string sender = 1;
  oneof contents {
    string message = 2;
  }
}
"""

v1_data = {
    "schema": V1_PROTO,
    "schemaType": "PROTOBUF",
}

# Test Case 10 - Updated
V2_PROTO = """
syntax = "proto3";

package message;
option go_package = "./message/v2;message";

message EnvelopeV2 {
  string sender = 1;
  oneof contents {
    string message = 2;
    string encoded_image = 3;
  }
}
"""

v2_data = {
    "schema": V2_PROTO,
    "schemaType": "PROTOBUF",
}

logging.debug(">>>> hello v1 proto")
register("hello", v1_data)

set_compatibility("hello", "BACKWARD_TRANSITIVE")

logging.debug(">>>> Registering hello v2 proto")
register("hello", v2_data)

