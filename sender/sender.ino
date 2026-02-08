#define SIGNAL_PIN 4      // Wire to ESP2
#define LED_PIN 2         // Built-in LED

void setup() {
  pinMode(SIGNAL_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
}

void loop() {
  // HIGH
  digitalWrite(SIGNAL_PIN, HIGH);
  digitalWrite(LED_PIN, HIGH);
  delay(500);

  // LOW
  digitalWrite(SIGNAL_PIN, LOW);
  digitalWrite(LED_PIN, LOW);
  delay(500);
}