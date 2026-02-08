#define SIGNAL_PIN 4
#define LED_PIN 2

void setup() {
  Serial.begin(115200);
  delay(2000);

  pinMode(SIGNAL_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);

  Serial.println("Sender Ready");
}

void loop() {
  // HIGH
  digitalWrite(SIGNAL_PIN, HIGH);
  digitalWrite(LED_PIN, HIGH);
  Serial.println("[SENDER] 1");
  delay(500);

  // LOW
  digitalWrite(SIGNAL_PIN, LOW);
  digitalWrite(LED_PIN, LOW);
  Serial.println("[SENDER] 0");
  delay(500);
}
