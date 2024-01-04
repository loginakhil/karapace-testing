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


CUSTOMER_PLACE_PROTO = """
syntax = "proto3";
package a1;
message Place {
        string city = 1;
        int32 zone = 2;
}
"""

customer_place_data = {
    "schema": CUSTOMER_PLACE_PROTO,
    "schemaType": "PROTOBUF",
}

CUSTOMER_PROTO = """
syntax = "proto3";
package a1;
import "place.proto";
import "google/type/postal_address.proto";
// @producer: another comment
message Customer {
        string name = 1;
        int32 code = 2;
        Place place = 3;
        google.type.PostalAddress address = 4;
}
"""

customer_data = {
    "schema": CUSTOMER_PROTO,
    "schemaType": "PROTOBUF",
    "references": [{
        "name": "place.proto",
        "subject": "place",
        "version": -1,
    }]
}

TEST_PROTO= """
syntax = "proto3";
package a1;
message Test {
        int32 id = 1;
}
"""

test_data = {
    "schema": TEST_PROTO,
    "schemaType": "PROTOBUF",
    "references": [{
        "name": "test.proto",
        "subject": "test",
        "version": -1,
    }]
}

CUSTOMER_PROTO_UPDATED = """
syntax = "proto3";
package a1;
import "place.proto";
import "test.proto";
import "google/type/postal_address.proto";
// @consumer: the comment was incorrect, updating it now
message Customer {
        string name = 1;
        int32 code = 2;
        Place place = 3;
        google.type.PostalAddress address = 4;
        Test test = 5;
}
"""

customer_data_updated = {
    "schema": CUSTOMER_PROTO_UPDATED,
    "schemaType": "PROTOBUF",
    "references": [{
        "name": "place.proto",
        "subject": "place",
        "version": -1,
    },{
        "name": "test.proto",
        "subject": "test",
        "version": -1,
    }]
}



logging.debug(">>>> List existing schemas")
get_all()
logging.debug(">>>> Registering place proto")
register("place", customer_place_data)
logging.debug(">>>> Registering customer proto")
register("customer", customer_data)
logging.debug(">>>> Registering test proto")
register("test", test_data)
logging.debug(">>>> Registering customer proto update")
register("customer", customer_data_updated)
