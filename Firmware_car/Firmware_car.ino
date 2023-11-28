#include <WiFi.h>

// Motor A
int motor1Pin1 = 27;
int motor1Pin2 = 26;
int enable1Pin = 14;

// Motor B
int motor2Pin1 = 23;
int motor2Pin2 = 22;
int enable2Pin = 12;

// Setting PWM properties
const int pwmChannel1 = 0;
const int pwmChannel2 = 1;
const int pwmFreq = 30000;
const int pwmResolution = 8;

// Wi-Fi settings
const char *ssid = "ESP32-Access-Point";
const char *password = "123456789";
WiFiServer server(80);

void setup() {
  Serial.begin(115200);

  pinMode(motor1Pin1, OUTPUT);
  pinMode(motor1Pin2, OUTPUT);
  pinMode(enable1Pin, OUTPUT);
  pinMode(motor2Pin1, OUTPUT);
  pinMode(motor2Pin2, OUTPUT);
  pinMode(enable2Pin, OUTPUT);

  ledcSetup(pwmChannel1, pwmFreq, pwmResolution);
  ledcSetup(pwmChannel2, pwmFreq, pwmResolution);

  ledcAttachPin(enable1Pin, pwmChannel1);
  ledcAttachPin(enable2Pin, pwmChannel2);
  
  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(100);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");

  server.begin();
}

void loop() {
  WiFiClient client = server.available();

  if (client) {
    Serial.println("New client connected");

    String command = "";
    while (client.connected()) {
      if (client.available()) {
        char c = client.read();

        if (c == '\n') {
          // End of command, process it
          Serial.println("Received command: " + command);
          processCommand(command, client);
          command = "";  // Clear the command for the next one
        } else {
          // Add the character to the current command
          command += c;
        }
      }
    }

    // Close the connection
    client.stop();
    Serial.println("Client disconnected");
  }
}

void processCommand(String command, WiFiClient &client) {
  if (command.startsWith("MOTOR1")) {
    // Example command: "MOTOR1 1 0 255"
    int status1 = command.charAt(7) - '0';
    int status2 = command.charAt(9) - '0';
    int dutyCycle = command.substring(11).toInt();

    // Update motor statuses and duty cycle
    digitalWrite(motor1Pin1, status1);
    digitalWrite(motor1Pin2, status2);
    ledcWrite(pwmChannel1, dutyCycle);

    Serial.println("Processed MOTOR1 command");
    client.print("MOTOR1 Command Processed");
  } else if (command.startsWith("MOTOR2")) {
    // Example command: "MOTOR2 1 0 200"
    int status1 = command.charAt(7) - '0';
    int status2 = command.charAt(9) - '0';
    int dutyCycle = command.substring(11).toInt();

    // Update motor statuses and duty cycle
    digitalWrite(motor2Pin1, status2);
    digitalWrite(motor2Pin2, status1);
    ledcWrite(pwmChannel2, dutyCycle);

    Serial.println("Processed MOTOR2 command");
    client.print("MOTOR2 Command Processed");
  } else {
    Serial.println("Unknown command: " + command);
    client.print("Unknown Command");
  }
}
