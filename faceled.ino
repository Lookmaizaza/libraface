const int relayPin = 15;  // Relay connected to GPIO 15

void setup() {
  Serial.begin(9600);
  pinMode(relayPin, OUTPUT);
  digitalWrite(relayPin, HIGH);  // Initially turn off the relay (assuming active LOW)
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    
    if (command == '1') {
      digitalWrite(relayPin, HIGH);  // Turn on relay
      Serial.println("Relay ON - No face or not recognized");
    } else if (command == '0') {
      digitalWrite(relayPin, LOW); // Turn off relay
      Serial.println("Relay OFF - Face recognized");
    }
  }
  
  delay(100);  // Small delay to stabilize
}