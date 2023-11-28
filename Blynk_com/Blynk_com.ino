/* Fill-in information from Blynk Device Info here */
#define BLYNK_TEMPLATE_ID "TMPL6GuSlbaLV"
#define BLYNK_TEMPLATE_NAME "CAR"
#define BLYNK_AUTH_TOKEN "2JW6gNnW3w3m1HexQS3EkjTwnLpD76LE"

/* Comment this out to disable prints and save space */
#define BLYNK_PRINT Serial

#define BOOT_BUTTON_PIN 0 // GPIO0 is commonly used for the boot button

#include <WiFi.h>
#include <WiFiClient.h>
#include <BlynkSimpleEsp32.h>

const int ledPin = 2; 
const int ledPin2 = 4; 

#include "Arduino.h"
bool toggleState = false;
bool buttonPressedOnce = false;
bool restartDone = false;

// Set password to "" for open networks.
char ssid[] = "iPhone";
char pass[] = "23452345";

int thresh = 0;

unsigned long lastBlinkTime = 0;
const unsigned long blinkInterval = 100; 
//
//const int analogPin1 = 4;  // Analog pin 4 (right)
//const int analogPin2 = 2;  // Analog pin 2 (center/front)
//const int analogPin3 = 15; // Analog pin 15 (left)

//
const int analogPin1 = 32;  // Analog pin 4 (right)
const int analogPin2 = 34;  // Analog pin 2 (center/front)
const int analogPin3 = 35; // Analog pin 15 (right)

// Motor A
int motor1Pin1 = 27; 
int motor1Pin2 = 26; 
int enable1Pin = 14; 

// Motor B
int motor2Pin1 = 23; 
int motor2Pin2 = 22; 
int enable2Pin = 12; 

// Setting PWM properties
const int freq = 30000;
const int pwmChannel1 = 0;
const int pwmChannel2 = 1;
const int resolution = 8;
int dutyCycle = 200;

int dutyCycleMotor1 = 0;  /
int dutyCycleMotor2 = 0;  

void setup() {
  pinMode(ledPin, OUTPUT);
  pinMode(ledPin2, OUTPUT);
  Serial.begin(115200);

  // sets the pins as outputs:
  pinMode(motor1Pin1, OUTPUT);
  pinMode(motor1Pin2, OUTPUT);
  pinMode(enable1Pin, OUTPUT);
  
  pinMode(motor2Pin1, OUTPUT);
  pinMode(motor2Pin2, OUTPUT);
  pinMode(enable2Pin, OUTPUT);

//  pinMode(analogPin1, INPUT);
//  pinMode(analogPin2, INPUT);
//  pinMode(analogPin3, INPUT);

  // configure PWM functionalities
  ledcSetup(pwmChannel1, freq, resolution);
  ledcSetup(pwmChannel2, freq, resolution);
  
  // attach the channels to the GPIOs to be controlled
  ledcAttachPin(enable1Pin, pwmChannel1);
  ledcAttachPin(enable2Pin, pwmChannel2);
  Blynk.begin(BLYNK_AUTH_TOKEN, ssid, pass);
  
}

void loop() {
  Blynk.run();

  if (Blynk.connected()){
    digitalWrite(ledPin, HIGH);
  }
  else{
    digitalWrite(ledPin, LOW);
  }
  

  
////  int buttonState = digitalRead(BOOT_BUTTON_PIN);
////  if (buttonState == LOW && !buttonPressedOnce) {
////    toggleState = !toggleState;
////    buttonPressedOnce = true;
////
////    while (toggleState) {
////      Serial.println("Button pressed - ON");
////      WiFi.disconnect();
////      Blynk.disconnect();
////      
////      int value1 = analogRead(analogPin1);
////      int value2 = analogRead(analogPin2);
////      int value3 = analogRead(analogPin3);
////    
////      Serial.print("Right: ");
////      Serial.print(value1);
////      Serial.print(" | Center: ");
////      Serial.print(value2);
////      Serial.print(" | Left: ");
////      Serial.println(value3);
////    
////      delay(100);
////      
////    } 
////    if(!toggleState) {
////      Serial.println("Button pressed - OFF");
////        // Check if toggleState is LOW, button has been pressed at least once, and restart is not done
////      if (toggleState == LOW && buttonPressedOnce && !restartDone) {
////        Serial.println("Performing esp.restart()");
////        delay(1000);  // Delay to allow serial print to complete
////        ESP.restart();
////        restartDone = true;  // Set restartDone to true to prevent further restarts
////      }
////      
//    }
//  }


}

BLYNK_WRITE(V2) {

  
  
  dutyCycleMotor1 = 0;
  dutyCycleMotor2 = 0;
  int x = param[0].asInt();
  int y = param[1].asInt();

  Serial.print("X = ");
  Serial.print(x);
  Serial.print("   Y = ");
  Serial.println(y);

  // Check if joystick is in the forward range
  if (y < 127 && x > 100 && x < 150) {
    Serial.println("Moving forward");
    digitalWrite(motor1Pin1, LOW);
    digitalWrite(motor1Pin2, HIGH);
    digitalWrite(motor2Pin1, HIGH);
    digitalWrite(motor2Pin2, LOW);
    dutyCycleMotor1 = map(y, 127, 0, 150, 255);
    dutyCycleMotor2 = map(y, 127, 0, 150, 255);
  }
  // Check if joystick is in the backward range
  else if (y > 128 && x > 100 && x < 150) {
    Serial.println("Moving backward");
    digitalWrite(motor1Pin1, HIGH);
    digitalWrite(motor1Pin2, LOW);
    digitalWrite(motor2Pin1, LOW);
    digitalWrite(motor2Pin2, HIGH);
    dutyCycleMotor1 = map(y, 128, 255, 150, 255);
    dutyCycleMotor2 = map(y, 128, 255, 150, 255);
  } 
  else if (y == 128 && x == 128) {
    Serial.println("Stop");
    digitalWrite(motor1Pin1, LOW);
    digitalWrite(motor1Pin2, LOW);
    digitalWrite(motor2Pin1, LOW);
    digitalWrite(motor2Pin2, LOW);
  }
  else {
    // Adjust duty cycles based on X-axis for turning
    if (x < 128) {
      Serial.println("Turning left");
    digitalWrite(motor1Pin1, HIGH);
    digitalWrite(motor1Pin2, LOW);
    digitalWrite(motor2Pin1, LOW);
    digitalWrite(motor2Pin2, HIGH);
//      int xMapped = map(x, 128, 0, 150, 255);
//      dutyCycleMotor1 = constrain(dutyCycle - xMapped, 0, 255);
//      dutyCycleMotor2 = constrain(dutyCycle + xMapped, 0, 255);
//
      dutyCycleMotor1 = map(x, 128, 0, 150, 200);
      dutyCycleMotor2 = map(x, 128, 0, 150, 255);

    } else if (x > 128) {
      Serial.println("Turning right");
    digitalWrite(motor1Pin1, HIGH);
    digitalWrite(motor1Pin2, LOW);
    digitalWrite(motor2Pin1, LOW);
    digitalWrite(motor2Pin2, HIGH);
//      int xMapped = map(x, 128, 255, 150, 255);
//      dutyCycleMotor1 = constrain(dutyCycle + xMapped, 0, 255);
//      dutyCycleMotor2 = constrain(dutyCycle - xMapped, 0, 255);
      dutyCycleMotor2 = map(x, 128, 255, 150, 200);
      dutyCycleMotor1 = map(x, 128, 255, 150, 255);

    } else {
      Serial.println("Joystick in the middle - no movement");
      dutyCycleMotor1 = 0;
      dutyCycleMotor2 = 0;
    }
  }

  Serial.print("Motor 1 Duty Cycle: ");
  Serial.println(dutyCycleMotor1);
  Serial.print("Motor 2 Duty Cycle: ");
  Serial.println(dutyCycleMotor2);

  ledcWrite(pwmChannel1, dutyCycleMotor1);
  ledcWrite(pwmChannel2, dutyCycleMotor2);

  delay(25);
}
