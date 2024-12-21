## Control Pi5 GPIO from MQTT 

JSON payload example:

```shell
{
    "name": "GPIO Name",
    "gpio": 30,
    "properties": {
        "direction": "out",
        "state": "on"
    }
}
```