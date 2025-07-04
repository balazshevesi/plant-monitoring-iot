def safe_publish(client, topic, message):
    try:
        client.publish(topic, message)
    except OSError as e:
        if e.args[0] == 104:
            print("Connection lost. Reconnecting...")
            client.connect()
            client.publish(topic, message)
        else:
            raise
