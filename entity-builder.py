import meshtastic.serial_interface

iface = meshtastic.serial_interface.SerialInterface()

gateway_id = "!6d00f4ac"
root_topic = "msh/2/json/LongFast"
node_list = ['!ced58391', '!215f357f']
use_node_list = True # only use nodes from the node list.  If False, create for all nodes in db.

include_messages = True
include_temperature = True
include_humidity = True
include_pressure = True
include_gas_resistance = False
include_power_ch1 = False
include_power_ch2 = False
include_power_ch3 = False

# initialize the file with the 'sensor' header
with open("mqtt.yaml", "w") as file:
    file.write('sensor:\n')  

for node_num, node in iface.nodes.items():
    print (node)

    node_short_name = f"{node['user']['shortName']}"
    node_long_name = f"{node['user']['longName']}"
    node_id = f"{node['user']['id']}"
    node_num = f"{node['num']}"
    hardware_model = f"{node['user']['hwModel']}"

    config = f'''
  - name: "{node_short_name} Battery Voltage"
    unique_id: "{node_short_name.lower().replace(" ", "_")}_battery_voltage"
    state_topic: "{root_topic}/{gateway_id}"
    state_class: measurement
    value_template: >-
      {{% if value_json.from == {node_num} and
          value_json.payload.voltage is defined and
          value_json.payload.temperature is not defined %}}
      {{{{ (value_json.payload.voltage | float) | round(2) }}}}
      {{% else %}}
        {{{{ states('sensor.{node_short_name.lower().replace(" ", "_")}_battery_voltage') }}}}
      {{% endif %}}
    unit_of_measurement: "V"
    icon: "mdi:lightning-bolt"
    device:
      identifiers: "meshtastic_{node_num}"

  - name: "{node_short_name} Battery Percent"
    unique_id: "{node_short_name.lower().replace(" ", "_")}_battery_percent"
    state_topic: "{root_topic}/{gateway_id}"
    state_class: measurement
    value_template: >-
      {{% if value_json.from == {node_num} and value_json.payload.battery_level is defined %}}
          {{{{ (value_json.payload.battery_level | float) | round(2) }}}}
      {{% else %}}
          {{{{ states('sensor.{node_short_name.lower().replace(" ", "_")}_battery_percent') }}}}
      {{% endif %}}
    unit_of_measurement: "%"
    icon: "mdi:battery-high"
    device:
      identifiers: "meshtastic_{node_num}"

  - name: "{node_short_name} ChUtil"
    unique_id: "{node_short_name.lower().replace(" ", "_")}_chutil"
    state_topic: "{root_topic}/{gateway_id}"
    state_class: measurement
    value_template: >-
      {{% if value_json.from == {node_num} and value_json.payload.channel_utilization is defined %}}
          {{{{ (value_json.payload.channel_utilization | float) | round(2) }}}}
      {{% else %}}
          {{{{ states('sensor.{node_short_name.lower().replace(" ", "_")}_chutil') }}}}
      {{% endif %}}
    unit_of_measurement: "%"
    icon: "mdi:signal-distance-variant"
    device:
      identifiers: "meshtastic_{node_num}"

  - name: "{node_short_name} AirUtilTX"
    unique_id: "{node_short_name.lower().replace(" ", "_")}_airutiltx"
    state_topic: "{root_topic}/{gateway_id}"
    state_class: measurement
    value_template: >-
      {{% if value_json.from == {node_num} and value_json.payload.air_util_tx is defined %}}
          {{{{ (value_json.payload.air_util_tx | float) | round(2) }}}}
      {{% else %}}
          {{{{ states('sensor.{node_short_name.lower().replace(" ", "_")}_airutiltx') }}}}
      {{% endif %}}
    unit_of_measurement: "%"
    icon: "mdi:percent-box-outline"
    device:
      identifiers: "meshtastic_{node_num}"
    '''

    if include_messages:
      config += f'''
  - name: "{node_short_name} Messages"
    unique_id: "{node_short_name.lower().replace(" ", "_")}_messages"
    state_topic: "{root_topic}/{gateway_id}"
    value_template: >-
      {{% if value_json.from == {node_num} and value_json.payload.text is defined %}}
          {{{{ value_json.payload.text }}}}
      {{% else %}}
          {{{{ states('sensor.{node_short_name.lower().replace(" ", "_")}_messages') }}}}
      {{% endif %}}
    device:
      identifiers: "meshtastic_{node_num}"
    icon: "mdi:chat"
        '''
      
    if include_temperature:
      config += f'''
  - name: "{node_short_name} Temperature"
    unique_id: "{node_short_name.lower().replace(" ", "_")}_temperature"
    state_topic: "{root_topic}/{gateway_id}"
    state_class: measurement
    value_template: >-
      {{% if value_json.from == {node_num} and value_json.payload.temperature is defined %}}
          {{{{ (((value_json.payload.temperature | float) * 1.8) +32) | round(2) }}}}
      {{% else %}}
          {{{{ states('sensor.{node_short_name.lower().replace(" ", "_")}_temperature') }}}}
      {{% endif %}}
    unit_of_measurement: "F"
    icon: "mdi:sun-thermometer"
    device:
      identifiers: "meshtastic_{node_num}"
    '''
      
    if include_humidity:
      config += f'''
  - name: "{node_short_name} Humidity"
    unique_id: "{node_short_name.lower().replace(" ", "_")}_humidity"
    state_topic: "{root_topic}/{gateway_id}"
    state_class: measurement
    value_template: >-
      {{% if value_json.from == {node_num} and value_json.payload.relative_humidity is defined %}}
          {{{{ (value_json.payload.relative_humidity | float) | round(2) }}}}
      {{% else %}}
          {{{{ states('sensor.{node_short_name.lower().replace(" ", "_")}_humidity') }}}}
      {{% endif %}}
    unit_of_measurement: "%"
    icon: "mdi:water-percent"
    device:
      identifiers: "meshtastic_{node_num}"
    '''
      
    if include_pressure:
      config += f'''
  - name: "{node_short_name} Pressure"
    unique_id: "{node_short_name.lower().replace(" ", "_")}_pressure"
    state_topic: "{root_topic}/{gateway_id}"
    state_class: measurement
    value_template: >-
      {{% if value_json.from == {node_num} and value_json.payload.barometric_pressure is defined %}}
          {{{{ (value_json.payload.barometric_pressure | float) | round(2) }}}}
      {{% else %}}
          {{{{ states('sensor.{node_short_name.lower().replace(" ", "_")}_pressure') }}}}
      {{% endif %}}
    unit_of_measurement: "hPa"
    icon: "mdi:chevron-double-down"
    device:
      identifiers: "meshtastic_{node_num}"
          '''
      
    if include_gas_resistance:
      config += f'''
  - name: "{node_short_name} Gas Resistance"
    unique_id: "{node_short_name.lower().replace(" ", "_")}_gas_resistance"
    state_topic: "{root_topic}/{gateway_id}"
    state_class: measurement
    value_template: >-
      {{% if value_json.from == {node_num} and value_json.payload.gas_resistance is defined %}}
          {{{{ (value_json.payload.gas_resistance | float) | round(2) }}}}
      {{% else %}}
          {{{{ states('sensor.{node_short_name.lower().replace(" ", "_")}_gas_resistance') }}}}
      {{% endif %}}
    unit_of_measurement: "MOhms"
    icon: "mdi:dots-hexagon"
    device:
      identifiers: "meshtastic_{node_num}"
          '''
    
    if include_power_ch1:
      config += f'''
  # {node_long_name}
  - name: "{node_short_name} Battery Voltage Ch1"
    unique_id: "{node_short_name.lower().replace(" ", "_")}_battery_voltage_ch1"
    state_topic: "{root_topic}/{gateway_id}"
    state_class: measurement
    value_template: >-
      {{% if value_json.from == {node_num} and value_json.payload.voltage_ch1 is defined %}}
      {{{{ (value_json.payload.voltage_ch1 | float) | round(2) }}}}
      {{% else %}}
        {{{{ states('sensor.{node_short_name.lower().replace(" ", "_")}_battery_voltage_ch1') }}}}
      {{% endif %}}
    unit_of_measurement: "V"
    icon: "mdi:lightning-bolt"
    device:
      identifiers: "meshtastic_{node_num}"

  - name: "{node_short_name} Battery Current Ch1"
    unique_id: "{node_short_name.lower().replace(" ", "_")}_battery_current_ch1"
    state_topic: "{root_topic}/{gateway_id}"
    state_class: measurement
    value_template: >-
      {{% if value_json.from == {node_num} and value_json.payload.current_ch1 is defined %}}
      {{{{ (value_json.payload.current_ch1 | float) | round(2) }}}}
      {{% else %}}
        {{{{ states('sensor.{node_short_name.lower().replace(" ", "_")}_battery_current_ch1') }}}}
      {{% endif %}}
    unit_of_measurement: "A"
    icon: "mdi:waves"
    device:
      identifiers: "meshtastic_{node_num}"
        '''
    
    if include_power_ch2:
      config += f'''
  - name: "{node_short_name} Battery Voltage Ch2"
    unique_id: "{node_short_name.lower().replace(" ", "_")}_battery_voltage_ch2"
    state_topic: "{root_topic}/{gateway_id}"
    state_class: measurement
    value_template: >-
      {{% if value_json.from == {node_num} and value_json.payload.voltage_ch2 is defined %}}
      {{{{ (value_json.payload.voltage_ch2 | float) | round(2) }}}}
      {{% else %}}
        {{{{ states('sensor.{node_short_name.lower().replace(" ", "_")}_battery_voltage_ch2') }}}}
      {{% endif %}}
    unit_of_measurement: "V"
    icon: "mdi:lightning-bolt"
    device:
      identifiers: "meshtastic_{node_num}"

  - name: "{node_short_name} Battery Current Ch2"
    unique_id: "{node_short_name.lower().replace(" ", "_")}_battery_current_ch2"
    state_topic: "{root_topic}/{gateway_id}"
    state_class: measurement
    value_template: >-
      {{% if value_json.from == {node_num} and value_json.payload.current_ch2 is defined %}}
      {{{{ (value_json.payload.current_ch2 | float) | round(2) }}}}
      {{% else %}}
        {{{{ states('sensor.{node_short_name.lower().replace(" ", "_")}_battery_current_ch2') }}}}
      {{% endif %}}
    unit_of_measurement: "A"
    icon: "mdi:waves"
    device:
      identifiers: "meshtastic_{node_num}"
    '''
      
    if include_power_ch3:
      config += f'''
  - name: "{node_short_name} Battery Voltage Ch3"
    unique_id: "{node_short_name.lower().replace(" ", "_")}_battery_voltage_ch3"
    state_topic: "{root_topic}/{gateway_id}"
    state_class: measurement
    value_template: >-
      {{% if value_json.from == {node_num} and value_json.payload.voltage_ch3 is defined %}}
      {{{{ (value_json.payload.voltage_ch3 | float) | round(2) }}}}
      {{% else %}}
        {{{{ states('sensor.{node_short_name.lower().replace(" ", "_")}_battery_voltage_ch3') }}}}
      {{% endif %}}
    unit_of_measurement: "V"
    icon: "mdi:lightning-bolt"
    device:
      identifiers: "meshtastic_{node_num}"

  - name: "{node_short_name} Battery Current Ch3"
    unique_id: "{node_short_name.lower().replace(" ", "_")}_battery_current_ch3"
    state_topic: "{root_topic}/{gateway_id}"
    state_class: measurement
    value_template: >-
      {{% if value_json.from == {node_num} and value_json.payload.current_ch3 is defined %}}
      {{{{ (value_json.payload.current_ch3 | float) | round(2) }}}}
      {{% else %}}
        {{{{ states('sensor.{node_short_name.lower().replace(" ", "_")}_battery_current_ch3') }}}}
      {{% endif %}}
    unit_of_measurement: "A"
    icon: "mdi:waves"
    device:
      identifiers: "meshtastic_{node_num}"
    '''


    if use_node_list:
      if node_id in node_list:
        with open("mqtt.yaml", "a") as file:
            file.write(config + '\n')
      
    else:
        with open("mqtt.yaml", "a") as file:
            file.write(config + '\n')
    

iface.close()