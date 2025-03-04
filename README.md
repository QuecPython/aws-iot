# AWS IoT Device Communication

## Overview
Guide to registering a device as a Thing in AWS IoT Core, setting up MQTT communication, and using IoT Device Shadows.

## Features
- Device registration and authentication
- MQTT-based messaging
- AWS IoT Shadow state management

### Register the Device
1. **Create an IoT Policy**: Allow necessary actions.
2. **Create a Thing**: Generate a certificate for authentication.

### MQTT Communication
- **Subscribe** to topics to receive messages.
- **Publish** messages to topics.
- **Use Callback Functions** for real-time updates.

### AWS IoT Device Shadow
- You can create Shadow in AwS IoT console or via program functions.
- **Key Operations**:
  - `update_shadow()`: Update state.
  - `get_shadow()`: Retrieve state.
  - `delete_shadow()`: Remove shadow.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Conclusion
Steps for AWS IoT Core device setup, MQTT communication, and device shadow management. For more in depth informations about using this library check docs/User_guide
