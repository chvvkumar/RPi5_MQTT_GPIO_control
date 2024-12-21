## Control Pi5 GPIO from MQTT 

JSON payload example:

```shell
{
    "name": "GPIO Name",
    "gpio": 21,
    "properties": {
        "direction": "out",
        "state": "on"
    }
}
```