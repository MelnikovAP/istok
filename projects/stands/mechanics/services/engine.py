def simulate(params: dict) -> dict:
    rpm = params.get("rpm", 1000)
    load = params.get("load", 0.5)
    torque = rpm * load * 0.01
    power = torque * rpm / 9549
    return {"rpm": rpm, "load": load, "torque": torque, "power": power}
