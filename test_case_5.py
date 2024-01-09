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


# Test Case 4 - Fuga 
FUGA_PROTO = """
syntax = "proto3";
package tc4;

import "google/protobuf/timestamp.proto";

enum GarplyType {
  GARPLY_TYPE_UNSPECIFIED = 0;
  GARPLY_TYPE_1 = 1;
  GARPLY_TYPE_2 = 2;
}

enum PlughType {
  PLUGH_TYPE_UNSPECIFIED = 0;
  PLUGH_TYPE_1 = 1;
  PLUGH_TYPE_2 = 2;
}

message Fred {
  string id = 1;
  string reference = 2;
  repeated Thud thuds = 3;
  google.protobuf.Timestamp fred_time = 4;
}

message Thud {
  string id = 1;
  uint32 num = 2;
}

message Hede {
  HedeType type = 1;
  string id = 2;
  Hodo hodo = 3;
}

enum HedeType {
  HEDE_TYPE_UNSPECIFIED = 0;
  HEDE_TYPE_1 = 1;
  HEDE_TYPE_2 = 2;
}

message Hodo {
  HodoCode code = 1;
  string id = 4;
}

enum HodoCode {
  HODO_CODE_UNSPECIFIED = 0;
  HODO_CODE_1 = 1;
  HODO_CODE_2 = 2;
}


"""

fuga_data = {
    "schema": FUGA_PROTO,
    "schemaType": "PROTOBUF",
}

# Test Case 4 - Toto 
TOTO_PROTO = """
syntax = "proto3";
package tc4;
message Toto {
  string id = 1;
  string ref = 2;
  uint32 num = 3;
}
"""

toto_data = {
    "schema": TOTO_PROTO,
    "schemaType": "PROTOBUF",
}

# Test Case 4 -  Fuga Updated
FUGA_UPDATED_PROTO = """
syntax = "proto3";
package tc4;

import "toto.proto";
import "google/protobuf/timestamp.proto";

enum GarplyType {
  GARPLY_TYPE_UNSPECIFIED = 0;
  GARPLY_TYPE_1 = 1;
  GARPLY_TYPE_2 = 2;
}

enum PlughType {
  PLUGH_TYPE_UNSPECIFIED = 0;
  PLUGH_TYPE_1 = 1;
  PLUGH_TYPE_2 = 2;
}

message Fred {
  string id = 1;
  string reference = 2;
  repeated Thud thuds = 3;
  google.protobuf.Timestamp fred_time = 4;
}

message Thud {
  string id = 1;
  uint32 num = 2;
  repeated Toto totos = 3;
}

message Hede {
  HedeType type = 1;
  string id = 2;
  Hodo hodo = 3;
}

enum HedeType {
  HEDE_TYPE_UNSPECIFIED = 0;
  HEDE_TYPE_1 = 1;
  HEDE_TYPE_2 = 2;
}

message Hodo {
  HodoCode code = 1;
  string id = 4;
}

enum HodoCode {
  HODO_CODE_UNSPECIFIED = 0;
  HODO_CODE_1 = 1;
  HODO_CODE_2 = 2;
}


"""

fuga_updated_data = {
    "schema": FUGA_UPDATED_PROTO,
    "schemaType": "PROTOBUF",
    "references": [{
        "name": "toto.proto",
        "subject": "toto",
        "version": -1,
    }]
}



logging.debug(">>>> Registering fuga proto")
register("fuga", fuga_data)

logging.debug(">>>> Registering toto proto")
register("toto", toto_data)

set_compatibility("fuga", "FULL_TRANSITIVE")
set_compatibility("toto", "FULL_TRANSITIVE")

logging.debug(">>>> Registering fuga updated proto")
register("fuga", fuga_updated_data)

