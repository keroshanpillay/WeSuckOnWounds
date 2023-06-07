const int sensorPin = A1; // Connect your sensor to analog pin A0

void setup() {
  Serial.begin(9600); // Begin serial communication at 9600 baud
}

void loop() {
  float voltage = analogRead(sensorPin) * (5.0 / 1023.0);
  Serial.println(voltage); // Send the sensor value to the computer
  delay(100); // Wait 100 milliseconds before the next reading
}
