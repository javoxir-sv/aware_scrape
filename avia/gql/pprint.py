import rich

# pretty prints JSON files
with open("payload/popular_destinations.json", "r") as file:
    payload = file.read()

rich.print_json(payload)

