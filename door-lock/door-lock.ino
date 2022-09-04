#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <ArduinoJson.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClient.h>

WiFiClient wifiClient;

String apUserName = "Door Lock";
String apPassword = "$dAAWdjaqje";
String staUserName;
String staPassword;
String authEndpoint;
String secret;

HTTPClient http;

ESP8266WebServer server(80);


int buttonPin = 14;
int outputPin = 12;

int redOutput=13;
int greenOutput=4;
int blueOutput = 5;

IPAddress local_ip(192,168,1,39);
IPAddress gateway(192,168,1,1);
IPAddress subnet(255, 255, 255, 0);

void setup() {
  Serial.begin(115200);

  WiFi.mode(WIFI_AP);
  WiFi.softAPConfig (local_ip, gateway, subnet);
  WiFi.softAP(apUserName, apPassword);

  
  // put your setup code here, to run once:
  pinMode(buttonPin, INPUT);
  pinMode(redOutput, OUTPUT);
  pinMode(greenOutput, OUTPUT);
  pinMode(blueOutput, OUTPUT);
  pinMode(outputPin, OUTPUT);
  Serial.println("Initialized");

  server.on("/", handle_index);
  server.on("/authres", handle_authCallback);
  server.onNotFound(handle_NotFound);
  server.begin();
  Serial.println("Server started");

  Serial.print("AcessPoint IP :");
  Serial.println(WiFi.softAPIP());
}

void loop() {
  // put your main code here, to run repeatedly:
  server.handleClient();

  if (isConnected()) {
    blueOn();
  } else {
    redOn();
  }
  if (digitalRead(buttonPin) == HIGH) {
      onButtonClicked();
  }
}

void handle_msg(int statusCode, String msg) {
    DynamicJsonDocument doc(1024);
    doc["data"] = msg;
    String json_obj;
    serializeJson(doc, json_obj);

    server.send(statusCode, "application/json", json_obj);
}

void handle_authCallback() {
  if (secret == nullptr || !isConnected()) {
    return handle_msg(400, "Please setup to continue");
  } 

  if (!server.hasArg("token")) {
    return handle_msg(401, "Token is required for this request!");
  }

  String token = server.arg("token");

  if (token.length() < 5  || token != secret) {
    return handle_msg(401, "Invalid token!");
  }

  handle_msg(200, "Door will be unlocked shortly!");
  openDoor();
}

bool isConnected() {
  if (WiFi.getMode() == WIFI_STA  && WiFi.status() == WL_CONNECTED) {
    return true;
  }
  return false;
}

void handle_index() {
  if (
      server.hasArg("ssid") && 
      server.hasArg("password") &&
      server.hasArg("secret") &&
      server.hasArg("endpoint")
    ) {
    staUserName = server.arg("ssid");
    staPassword = server.arg("password");
    authEndpoint = server.arg("endpoint");
    secret = server.arg("secret");

    return initializeWifi();
  }

  
  if (WiFi.getMode() == WIFI_STA) {
    
    String wifiStatus = "not connected yet";
    if (isConnected()) {
       wifiStatus = "connected";
    }
    
    server.send(200, "text/plain", 
    "Configured with status " + wifiStatus + " to " + staUserName 
    );
  } else {
      server.send(200, "text/html", send_setup());
  }
}

void handle_NotFound(){
  server.send(404, "text/plain", "Not found");
}

void openDoor() {
  Serial.println("open door");
  digitalWrite(outputPin, HIGH);
  delay(6000);
  digitalWrite(outputPin, LOW);
}

void initializeWifi() {
  WiFi.mode(WIFI_STA);
  WiFi.config(local_ip, gateway, subnet);
  WiFi.begin(staUserName, staPassword);
  Serial.print("Connecting ");
  while (WiFi.status() != WL_CONNECTED) 
  {
     delay(500);
     Serial.print("*");
  }

  
  Serial.print("Station IP :");
  Serial.println(WiFi.localIP());
  server.send(
    200, 
    "text/plain", 
    "Connected to the requested network. Access Point will now disconnect"
  );
  WiFi.softAPdisconnect(true);
}

void clearLed() {
  for (int clr :{greenOutput, redOutput, blueOutput}) {
    digitalWrite(clr, LOW);
  }
}

void greenOn() { clearLed(); digitalWrite(greenOutput, HIGH);}

void redOn() { clearLed(); digitalWrite(redOutput, HIGH);}

void blueOn() { clearLed(); digitalWrite(blueOutput, HIGH);}

void onButtonClicked() {
  if (!isConnected()) {
    return;
  }

  Serial.println("Button has been clicked"); 
  String url = authEndpoint + "?token=" + secret + "&event=authorize&data=button";
  http.begin(wifiClient, url);
  int httpStatusCode = http.GET();
  Serial.println("http request status code");
  Serial.println("url " + url);
  Serial.println(httpStatusCode);
  Serial.println(http.getString());
  if (httpStatusCode > 0 && httpStatusCode >= 200 && httpStatusCode < 300) {
    greenOn();
  } else {
    redOn();
  }
  delay(4000);
}

String send_setup() {
  int networkCount = WiFi.scanNetworks();
  String html_str = R"html(
  <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Setup Door Lock</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">


    <style>
        .setup-container {
            max-width: 400px;
        }

        .setup-container h1,
        .setup-container h3 {
            margin-top: 0;
            margin-bottom: 0;
        }

        .setup-container h3 {
            margin-bottom: 30px;
        }

        .setup-container input,
        .setup-container select {
            width: calc(100% - 20px);
            margin-bottom: 20px;
            padding: 5px 10px;
            color: #333;
            font-size: 16px;
        }
    </style>
</head>
<body>

<div class="setup-container">
    <form method="post">
    <h1>To configure</h1>
    <h3>Please select your SSID and password</h3>

    <label for="avail-network">Available Network</label>
    <select id="avail-network" name="ssid">
)html";

for (int i = 0; i < networkCount; i++) {
  html_str +="<option value='"+WiFi.SSID(i)+"'>"+WiFi.SSID(i)+"</option>";
}

html_str +=R"html(   
    </select>
    <br>
    <label for="network-password">Network Password</label>
    <input autocomplete="off" id="network-password" type="password" name="password">


    <label for="secret">Auth Secret</label>
    <input id="secret" type="text" name="secret">
        
        
    <label for="endpoint">Server Endpoint</label>
    <input id="endpoint" type="url" name="endpoint">
        
    <button type="submit">Setup</button>
    </form>
</div>
</body>
</html>
)html";

  return html_str;
}
