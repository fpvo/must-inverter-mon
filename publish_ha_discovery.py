import json
import subprocess

DEVICE = {
    "identifiers": ["must_pv18_inverter"],
    "name": "MUST PV18 Solar Inverter",
    "manufacturer": "MUST",
    "model": "PV18-1012VPM II"
}

SENSORS = [
    {"key": "battery_v", "name": "Solar Battery Voltage", "unit": "V", "device_class": "voltage"},
    {"key": "battery_current", "name": "Solar Battery Current", "unit": "A", "device_class": "current"},
    {"key": "inverter_v", "name": "Solar Inverter Voltage", "unit": "V", "device_class": "voltage"},
    {"key": "inverter_current", "name": "Solar Inverter Current", "unit": "A", "device_class": "current"},
    {"key": "grid_v", "name": "Solar Grid Voltage", "unit": "V", "device_class": "voltage"},
    {"key": "grid_freq", "name": "Solar Grid Frequency", "unit": "Hz", "device_class": "frequency"},
    {"key": "grid_power", "name": "Solar Grid Power", "unit": "W", "device_class": "power"},
    {"key": "load_power", "name": "Solar Load Power", "unit": "W", "device_class": "power"},
    {"key": "bus_v", "name": "Solar DC Bus Voltage", "unit": "V", "device_class": "voltage"},
    {"key": "temperature", "name": "Solar Inverter Temperature", "unit": "°C", "device_class": "temperature"},
    {"key": "error_code", "name": "Solar Error Code", "unit": None, "device_class": None},
    {"key": "warning_code", "name": "Solar Warning Code", "unit": None, "device_class": None},
]

WORK_STATE_TEMPLATE = (
    "{% set states = {'0':'PowerOn','1':'SelfTest','2':'OffGrid','3':'Grid-Tie',"
    "'4':'ByPass','5':'Stop','6':'GridCharging'} %}"
    "{{ states.get(value, 'Unknown(' ~ value ~ ')') }}"
)

def publish(topic, payload):
    subprocess.run(
        ["docker", "exec", "mosquitto", "mosquitto_pub", "-r", "-t", topic, "-m", json.dumps(payload)],
        check=True
    )

for s in SENSORS:
    topic = f"homeassistant/sensor/must_pv18/{s['key']}/config"
    payload = {
        "name": s["name"],
        "unique_id": f"must_pv18_{s['key']}",
        "state_topic": f"home/solar/{s['key']}",
        "device": DEVICE,
        "state_class": "measurement",
    }
    if s["unit"]:
        payload["unit_of_measurement"] = s["unit"]
    if s["device_class"]:
        payload["device_class"] = s["device_class"]
    publish(topic, payload)
    print(f"published {topic}")

# work_state gets a value_template decoding the numeric code to a friendly string
work_state_payload = {
    "name": "Solar Work State",
    "unique_id": "must_pv18_work_state",
    "state_topic": "home/solar/work_state",
    "value_template": WORK_STATE_TEMPLATE,
    "device": DEVICE,
}
publish("homeassistant/sensor/must_pv18/work_state/config", work_state_payload)
print("published homeassistant/sensor/must_pv18/work_state/config")
