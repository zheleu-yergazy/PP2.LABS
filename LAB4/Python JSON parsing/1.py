import json


with open(r"C:\Users\Madina Zheleu\OneDrive\Рабочий стол\lab\LAB1\LAB4\Python JSON parsing\sample-data.json") as f:
    data = json.load(f)


print("Interface Status")
print("=" * 80)
print(f"{'DN':<50} {'Description':<20} {'Speed':<7} {'MTU':<7}")
print("-" * 80)


for item in data["imdata"]:
    attributes = item["l1PhysIf"]["attributes"]
    dn = attributes["dn"]
    descr = attributes.get("descr", "")
    speed = attributes.get("speed", "")
    mtu = attributes.get("mtu", "")
    

    print(f"{dn:<50} {descr:<20} {speed:<7} {mtu:<7}")
