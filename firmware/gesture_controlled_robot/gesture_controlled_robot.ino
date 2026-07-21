#include <ESP8266WiFi.h>

const char* ssid = "RobotCar";
const char* password = "YOUR_ROBOT_WIFI_PASSWORD";

WiFiServer server(80);

// Motor pins
int IN1 = D1;
int IN2 = D2;
int IN3 = D5;
int IN4 = D6;

void setup() {

  Serial.begin(115200);

  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  stopRobot();

  WiFi.softAP(ssid, password);
  server.begin();

  Serial.println("Robot WiFi Started");
  Serial.print("IP Address: ");
  Serial.println(WiFi.softAPIP());
}

void forward(){
  Serial.println("FORWARD");

  digitalWrite(IN1,HIGH);
  digitalWrite(IN2,LOW);
  digitalWrite(IN3,HIGH);
  digitalWrite(IN4,LOW);
}

void backward(){
  Serial.println("BACKWARD");

  digitalWrite(IN1,LOW);
  digitalWrite(IN2,HIGH);
  digitalWrite(IN3,LOW);
  digitalWrite(IN4,HIGH);
}

void left(){
  Serial.println("LEFT");

  digitalWrite(IN1,LOW);
  digitalWrite(IN2,HIGH);
  digitalWrite(IN3,HIGH);
  digitalWrite(IN4,LOW);
  delay(400);   

  stopRobot();
  delay(100);

  // Step 2: Move forward
  forward();
}

void right(){
  Serial.println("RIGHT");

  digitalWrite(IN1,HIGH);
  digitalWrite(IN2,LOW);
  digitalWrite(IN3,LOW);
  digitalWrite(IN4,HIGH);
  delay(400);  

  stopRobot();
  delay(100);

  // Step 2: Move forward
  forward();
}

void stopRobot(){
  Serial.println("STOP");

  digitalWrite(IN1,LOW);
  digitalWrite(IN2,LOW);
  digitalWrite(IN3,LOW);
  digitalWrite(IN4,LOW);
}

void loop() {

  WiFiClient client = server.available();
  if (!client) return;

  Serial.println("Client Connected");

  while(!client.available()){
    delay(1);
  }

  String request = client.readStringUntil('\r');
  Serial.println(request);

  if(request.indexOf("/forward")!=-1) forward();
  else if(request.indexOf("/back")!=-1) backward();
  else if(request.indexOf("/left")!=-1) left();
  else if(request.indexOf("/right")!=-1) right();
  else if(request.indexOf("/stop")!=-1) stopRobot();

  // HTTP response
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/plain");
  client.println("Connection: close");
  client.println("Content-Length: 2");
  client.println();
  client.print("OK");

  delay(1);
  client.stop();

}
