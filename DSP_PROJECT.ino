#include "WiFi.h"
#include <HTTPClient.h>
#include "time.h"
#include "DHT.h"

#define DHTPIN 22
#define DHTTYPE DHT11

const char* ntpServer1 = "pool.ntp.org";
const char* ntpServer2 = "time.nist.gov";
const long gmtOffset_sec = 28800;
const int daylightOffset_sec = 0;
float h = 0.0;
float t = 0.0;

char ssid[] = "Sumagui_PLDT";
char password[] = "G@brieL03202002!@";

DHT dht(DHTPIN, DHTTYPE);

String GOOGLE_SCRIPT_ID = "AKfycbz7uiGSdJVUSp-DlRQaF59o7KeZCjiYjN8-euw6s8rFcwqSLjLbrujSf0X7Ik-5ya3a";

void setup() {

  delay(1000);
  Serial.begin(115200);
  dht.begin();
  delay(1000);
  Serial.println();
  Serial.print("Connecting to wifi: ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");

  }
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer1, ntpServer2);
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    SendDataToGoogleSheets();
  }
}

void SendDataToGoogleSheets() {
  // Read data from the DHT sensor
  float newH = dht.readHumidity();
  float newT = dht.readTemperature();

  if (isnan(newH) || isnan(newT)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

  h = newH;
  t = newT;

  Serial.print(F("Humidity: "));
  Serial.print(h);
  Serial.print(F("%  Temperature: "));
  Serial.print(t);
  Serial.print(F("°C "));

  // Get the current time
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo)) {
    Serial.println("Failed to obtain time");
    return;
  } else {
    char timeStringBuff[50];
    strftime(timeStringBuff, sizeof(timeStringBuff), "%m/%d/%Y_%H:%M:%S", &timeinfo);
    String asString(timeStringBuff);
    Serial.print("Time:");
    Serial.println(asString);

    // Create the URL for the Google Sheets script
    String urlFinal = "https://script.google.com/macros/s/" + GOOGLE_SCRIPT_ID + "/exec?" +
                     "date=" + asString + "&humi=" + String(h) + "&temp=" + String(t);
    Serial.print("POST data to spreadsheet:");
    Serial.println(urlFinal);

    // Send the data to Google Sheets
    HTTPClient http;
    http.begin(urlFinal.c_str());
    http.setFollowRedirects(HTTPC_STRICT_FOLLOW_REDIRECTS);
    int httpCode = http.GET();
    Serial.print("HTTP Status Code: ");
    Serial.println(httpCode);

    if (httpCode == 200) {
      delay(180000); // Wait for 3 minutes
    }
    http.end();
    delay(720000); // Wait for 12 minutes before the next data transmission
  }
}
