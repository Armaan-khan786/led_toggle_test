#define SIGNAL_PIN 4
#define LED_PIN 2

void setup() {
  Serial.begin(115200);
  delay(3000);   // allow full boot after flashing

  pinMode(SIGNAL_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);

  digitalWrite(SIGNAL_PIN, LOW);   // force known start state
  digitalWrite(LED_PIN, LOW);

  Serial.println("Sender Ready");
}

void loop() {
  digitalWrite(SIGNAL_PIN, HIGH);
  digitalWrite(LED_PIN, HIGH);
  Serial.println("[SENDER] 1");
  delay(500);

  digitalWrite(SIGNAL_PIN, LOW);
  digitalWrite(LED_PIN, LOW);
  Serial.println("[SENDER] 0");
  delay(500);
}
