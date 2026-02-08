#define SIGNAL_PIN 4
#define LED_PIN 2

int lastState = -1;

void setup() {
  Serial.begin(115200);
  delay(2000);

  pinMode(SIGNAL_PIN, INPUT_PULLDOWN);
  pinMode(LED_PIN, OUTPUT);

  Serial.println("Receiver Ready");
}

void loop() {
  int state = digitalRead(SIGNAL_PIN);

  digitalWrite(LED_PIN, state);

  if (state != lastState) {
    if (state == HIGH)
      Serial.println("[RECEIVER] 1");
    else
      Serial.println("[RECEIVER] 0");

    lastState = state;
  }
}
