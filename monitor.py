#define SIGNAL_PIN 4
#define LED_PIN 2

int lastState = -1;

void setup() {
  Serial.begin(115200);
  delay(3000);   // give time after flashing/reset

  pinMode(SIGNAL_PIN, INPUT_PULLDOWN);
  pinMode(LED_PIN, OUTPUT);

  Serial.println("Receiver Ready");
}

void loop() {
  int state = digitalRead(SIGNAL_PIN);

  digitalWrite(LED_PIN, state);

  if (state != lastState) {
    Serial.print("[RECEIVER] ");
    Serial.println(state);
    lastState = state;
  }

  delay(50);   // stability delay
}
