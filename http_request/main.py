from ic.client import Client
from ic.identity import Identity
from ic.agent import Agent
from ic.canister import Canister
from pathlib import Path

# Identity and Client are dependencies of Agent
iden = Identity()  # creates a random keypair
client = Client()  # creates a client to talk to the IC
# creates an agent, combination of client and identity
agent = Agent(iden, client)

http_gateway_did = open(Path(__file__).parent / "http-gateway.did").read()


def retrieve_html(canister_id: str, path: str) -> str:
    # create a canister with the http gateway did
    asset_canister = Canister(
        agent=agent, canister_id=canister_id, candid=http_gateway_did
    )
    result = asset_canister.http_request({"method": "GET", "url": path, "headers": [], "body": []})  # type: ignore
    # decode a vector of bytes to a string
    return "".join(chr(n) for n in result[0]["body"])


def write_html(html: str, path: str):
    # write html to a file
    with open(path, "w") as f:
        f.write(html)


html = retrieve_html("g3jne-7iaaa-aaaal-ab73a-cai", "/")
write_html(html, "index.html")
