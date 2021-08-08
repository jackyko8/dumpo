# Dumpo Python Object Serialiser

Dumpo serialises a Python object recursively to arbitrary levels, optionally in a JSON like format.

Synopsis:
```python
from dumpo import dumpo
obj_str = dumpo(obj)
print(obj_str)
```

Keyword arguments:

| Argument          | Description                                                  | Type            | Default Value |
| ----------------- | ------------------------------------------------------------ | --------------- | ------------- |
| as_is             | Data type name or list of them to be shown as is. i.e., `f'{obj}'` | List or string | `[]`          |
| as_is_tag         | String to append to a data item serialised "as is"           | String          | `"<as_is>"` |
| code_tag | String to replace function code | String | `"<code>"` |
| compressed        | If True compress list to a single line instead of one data item per line | Boolean         | `True`        |
| debug             | If True append debug information to each data item, e.g., data type, quotes to use and iterator | Boolean         | `False`       |
| deep_types | Data type names or list of them to be shown even the item is at level `maxdepth+1` | List or string | `[]` |
| excluded          | Data item names or list of them to be excluded from serialisation | List or string  | `[]`          |
| excluded_tag      | String to replace excluded data items. Blank to hide all excluded data items. | String        | `"<excluded>"` |
| expand_keys       | If True serialise structured item keys, else show them as a string. i.e., `print(f'{itemKey}')` | Boolean         | `False`       |
| include_all_keys  | If True include all keys including internal ones (`_<name>`) and built-in ones (`__<name>`) excluding `__dict__`. | Boolean | `False` |
| include_everything | Equivalent to `include_all_keys=True, include_functions=True, expand_keys=True`, with `__dict__` included. | Boolean | `False` |
| include_internals | If True include internal keys (`_<name>`) but not built-in ones (`__<name>`). | Boolean | `False` |
| include_functions | If True include object function names (including internal functions if `include_all_keys` is also True). | Boolean         | `False`       |
| indent            | String used for indentation, repeat for the number of levels | String          | `"\| "`   |
| item_quotes       | Quotation marks for item keys - a 2-character string for open and close respectively; a 1-character string if open and close are the same; blank means no quotation marks for item keys | String          | `None`        |
| json_like         | If True serialise in JSON format - implying `indent="  "` and `item_quotes = '"'`, and `False` for `show_types` and `show_all_types`. | Boolean         | `False`       |
| maxdepth          | Maximum levels to serialise                                  | Integer         | `5`           |
| quotes            | Quotation marks for data items - a 2-character string for open and close respectively; a 1-character string if open and close are the same; blank means no quotation marks for data items | String          | `""`  |
| show_all_types    | If True prepend the data type to each data item of all types, e.g., `<type>{ ... }`    | Boolean       | `True`        |
| show_types        | If True prepend the data type to each data item except for simple types, e.g., `<type>{ ... }` | Boolean        | `True`        |
| too_deep_tag      | String to replace data items or structures below the `maxdepth`th level | String         | `"<too_deep>"` |

[Dumpo at GitHub](https://github.com/jackyko8/dumpo)

## Examples

```python
>>> from dumpo import dumpo
>>> import boto3
>>> ec2 = boto3.client('ec2')
>>> response = ec2.describe_instances()
>>> print(dumpo(response, maxdepth=1))
{
| Reservations: [ <too_deep>, <too_deep>, <too_deep>, <too_deep>, <too_deep>, <too_deep>, <too_deep>, <too_deep>, <too_deep>, <too_deep> ],
| ResponseMetadata: {
| | RequestId: <too_deep>,
| | HTTPStatusCode: <too_deep>,
| | HTTPHeaders: <too_deep>,
| | RetryAttempts: <too_deep>
| }
}
>>> print(dumpo(response['Reservations'][0], maxdepth=1))
{
| Groups: [],
| Instances: [ <too_deep> ],
| OwnerId: "999999999999",
| ReservationId: "r-xxxxxxxxxxxxxxxxx"
}
>>> print(dumpo(response['Reservations'][0]['Instances'][0], too_deep_tag='...'))
{
| AmiLaunchIndex: 0,
| ImageId: "ami-xxxxxxxxxxxxxxxxx",
| InstanceId: "i-xxxxxxxxxxxxxxxxx",
| InstanceType: "x9.xxxx",
| KeyName: "xxx",
| LaunchTime: <datetime>yyyy-mm-dd HH:MM:SS+00:00,
| Monitoring: {'State': 'disabled'},
| Placement: {'AvailabilityZone': 'xx-xxxxxx-9x', 'GroupName': '', 'Tenancy': 'default'},
| PrivateDnsName: "ip-99-99-99-99.xx-xxxxxx-9.compute.internal",
| PrivateIpAddress: "99.99.99.99",
| ProductCodes: [],
| PublicDnsName: "",
| State: {'Code': 80, 'Name': 'stopped'},
| StateTransitionReason: "User initiated (yyyy-mm-dd HH:MM:SS GMT)",
| SubnetId: "subnet-xxxxxxxx",
| VpcId: "vpc-xxxxxxxx",
| Architecture: "x86_64",
| BlockDeviceMappings: [ {
| | | DeviceName: "/dev/xvda",
| | | Ebs: {'AttachTime': datetime.datetime(yyyy, mm, dd, HH, MM, SS, tzinfo=tzutc()), 'DeleteOnTermination': True, 'Status': 'attached', 'VolumeId': 'vol-xxxxxxxxxxxxxxxxx'}
| | } ],
| ClientToken: "",
| EbsOptimized: False,
| EnaSupport: True,
| Hypervisor: "xen",
| NetworkInterfaces: [ {
| | | Attachment: {'AttachTime': datetime.datetime(yyyy, mm, dd, HH, MM, SS, tzinfo=tzutc()), 'AttachmentId': 'eni-attach-0eb44e06cead04be4', 'DeleteOnTermination': True, 'DeviceIndex': 0, 'Status': 'attached', 'NetworkCardIndex': 0},
| | | Description: "Primary network interface",
| | | Groups: [ {
| | | | | GroupName: "ssh-xxx",
| | | | | GroupId: "sg-xxxxxxxxxxxxxxxxx"
| | | | } ],
| | | Ipv6Addresses: [],
| | | MacAddress: "xx:xx:xx:xx:xx:xx",
| | | NetworkInterfaceId: "eni-xxxxxxxxxxxxxxxxx",
| | | OwnerId: "999999999999",
| | | PrivateDnsName: "ip-99-99-99-99.xx-xxxxxx-9.compute.internal",
| | | PrivateIpAddress: "99.99.99.99",
| | | PrivateIpAddresses: [ {
| | | | | Primary: True,
| | | | | PrivateDnsName: "ip-99-99-99-99.xx-xxxxxx-9.compute.internal",
| | | | | PrivateIpAddress: "99.99.99.99"
| | | | } ],
| | | SourceDestCheck: True,
| | | Status: "in-use",
| | | SubnetId: "subnet-xxxxxxxx",
| | | VpcId: "vpc-xxxxxxxx",
| | | InterfaceType: "interface"
| | } ],
| RootDeviceName: "/dev/xvda",
| RootDeviceType: "ebs",
| SecurityGroups: [ {
| | | GroupName: "ssh-xxx",
| | | GroupId: "sg-xxxxxxxxxxxxxxxxx"
| | } ],
| SourceDestCheck: True,
| StateReason: {'Code': 'Client.UserInitiatedShutdown', 'Message': 'Client.UserInitiatedShutdown: User initiated shutdown'},
| Tags: [ {
| | | Key: "Name",
| | | Value: "xxx"
| | } ],
| VirtualizationType: "hvm",
| CpuOptions: {'CoreCount': 1, 'ThreadsPerCore': 1},
| CapacityReservationSpecification: {'CapacityReservationPreference': 'open'},
| HibernationOptions: {'Configured': False},
| MetadataOptions: {'State': 'applied', 'HttpTokens': 'optional', 'HttpPutResponseHopLimit': 1, 'HttpEndpoint': 'enabled'},
| EnclaveOptions: {'Enabled': False}
}
>>> print(dumpo(response['Reservations'][0]['Instances'][0], too_deep_tag='...', json_like=True))
{
  "AmiLaunchIndex": 0,
  "ImageId": "ami-xxxxxxxxxxxxxxxxx",
  "InstanceId": "i-xxxxxxxxxxxxxxxxx",
  "InstanceType": "x9.xxxx",
  "KeyName": "xxx",
  "LaunchTime": "yyyy-mm-dd HH:MM:SS+00:00",
  "Monitoring": {
    "State": "disabled"
  },
  "Placement": {
    "AvailabilityZone": "xx-xxxxxx-9x",
    "GroupName": "",
    "Tenancy": "default"
  },
  "PrivateDnsName": "ip-99-99-99-99.xx-xxxxxx-9.compute.internal",
  "PrivateIpAddress": "99.99.99.99",
  "ProductCodes": "[]",
  "PublicDnsName": "",
  "State": {
    "Code": 80,
    "Name": "stopped"
  },
  "StateTransitionReason": "User initiated (yyyy-mm-dd HH:MM:SS GMT)",
  "SubnetId": "subnet-xxxxxxxx",
  "VpcId": "vpc-xxxxxxxx",
  "Architecture": "x86_64",
  "BlockDeviceMappings": [ {
      "DeviceName": "/dev/xvda",
      "Ebs": {
        "AttachTime": "yyyy-mm-dd HH:MM:SS+00:00",
        "DeleteOnTermination": "True",
        "Status": "attached",
        "VolumeId": "vol-xxxxxxxxxxxxxxxxx"
      }
    } ],
  "ClientToken": "",
  "EbsOptimized": "False",
  "EnaSupport": "True",
  "Hypervisor": "xen",
  "NetworkInterfaces": [ {
      "Attachment": {
        "AttachTime": "yyyy-mm-dd HH:MM:SS+00:00",
        "AttachmentId": "eni-attach-xxxxxxxxxxxxxxxxx",
        "DeleteOnTermination": "True",
        "DeviceIndex": 0,
        "Status": "attached",
        "NetworkCardIndex": 0
      },
      "Description": "Primary network interface",
      "Groups": [ {
          "GroupName": "ssh-xxx",
          "GroupId": "sg-xxxxxxxxxxxxxxxxx"
        } ],
      "Ipv6Addresses": "[]",
      "MacAddress": "xx:xx:xx:xx:xx:xx",
      "NetworkInterfaceId": "eni-xxxxxxxxxxxxxxxxx",
      "OwnerId": "999999999999",
      "PrivateDnsName": "ip-99-99-99-99.xx-xxxxxx-9.compute.internal",
      "PrivateIpAddress": "99.99.99.99",
      "PrivateIpAddresses": [ {
          "Primary": "True",
          "PrivateDnsName": "ip-99-99-99-99.xx-xxxxxx-9.compute.internal",
          "PrivateIpAddress": "99.99.99.99"
        } ],
      "SourceDestCheck": "True",
      "Status": "in-use",
      "SubnetId": "subnet-xxxxxxxx",
      "VpcId": "vpc-xxxxxxxx",
      "InterfaceType": "interface"
    } ],
  "RootDeviceName": "/dev/xvda",
  "RootDeviceType": "ebs",
  "SecurityGroups": [ {
      "GroupName": "ssh-xxx",
      "GroupId": "sg-xxxxxxxxxxxxxxxxx"
    } ],
  "SourceDestCheck": "True",
  "StateReason": {
    "Code": "Client.UserInitiatedShutdown",
    "Message": "Client.UserInitiatedShutdown: User initiated shutdown"
  },
  "Tags": [ {
      "Key": "Name",
      "Value": "xxx"
    } ],
  "VirtualizationType": "hvm",
  "CpuOptions": {
    "CoreCount": 1,
    "ThreadsPerCore": 1
  },
  "CapacityReservationSpecification": {
    "CapacityReservationPreference": "open"
  },
  "HibernationOptions": {
    "Configured": "False"
  },
  "MetadataOptions": {
    "State": "applied",
    "HttpTokens": "optional",
    "HttpPutResponseHopLimit": 1,
    "HttpEndpoint": "enabled"
  },
  "EnclaveOptions": {
    "Enabled": "False"
  }
}
```

