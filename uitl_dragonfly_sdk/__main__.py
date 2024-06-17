from uitl_dragonfly_sdk.DragonflyClient import DragonflyClient

print("hello world!")

client = DragonflyClient("cid", "sec", "https://auth.dragonflydatahq.com/realms/dragonfly", "api")
output = client.run_health_report(1)

print(output)
