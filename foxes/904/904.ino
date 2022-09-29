#include <RFM69OOK.h>
#include <ArduinoLowPower.h>

#define RFM69_CS      8
#define RFM69_INT     3
#define RFM69_RST     4
#define LED           13

char message[] = "this is ve3irr/w3   -   the flag is shuffleboard";
unsigned long dit_len = 100; /* 12 WPM */

RFM69OOK radio(RFM69_CS, RFM69_INT, true, 0);

void setup() {
  radio.initialize();
  radio.transmitBegin();
  radio.setFrequencyMHz(904.45);
  radio.setPowerLevel(16);
  pinMode(LED_BUILTIN, OUTPUT);
}

void dit() {
  radio.transmitBegin();
  digitalWrite(LED_BUILTIN, HIGH);
  delay(dit_len);
  digitalWrite(LED_BUILTIN, LOW);
  radio.transmitEnd();
  delay(dit_len);
}

void dah() {
  radio.transmitBegin();
  digitalWrite(LED_BUILTIN, HIGH);
  delay(dit_len * 3);
  digitalWrite(LED_BUILTIN, LOW);
  radio.transmitEnd();
  delay(dit_len);
}

void end() {
  delay(dit_len * 2);
}

void space() {
  delay(dit_len * 4);
}

void loop() {
  for (char *it = message; *it; it++) {
    switch(*it) {
      case 'a': dit(); dah(); break;
      case 'b': dah(); dit(); dit(); dit(); break;
      case 'c': dah(); dit(); dah(); dit(); break;
      case 'd': dah(); dit(); dit(); break;
      case 'e': dit(); break;
      case 'f': dit(); dit(); dah(); dit(); break;
      case 'g': dah(); dah(); dit(); break;
      case 'h': dit(); dit(); dit(); dit(); break;
      case 'i': dit(); dit(); break;
      case 'j': dit(); dah(); dah(); dah(); break;
      case 'k': dah(); dit(); dah(); break;
      case 'l': dit(); dah(); dit(); dit(); break;
      case 'm': dah(); dah(); break;
      case 'n': dah(); dit(); break;
      case 'o': dah(); dah(); dah(); break;
      case 'p': dit(); dah(); dah(); dit(); break;
      case 'q': dah(); dah(); dit(); dah(); break;
      case 'r': dit(); dah(); dit(); break;
      case 's': dit(); dit(); dit(); break;
      case 't': dah(); break;
      case 'u': dit(); dit(); dah(); break;
      case 'v': dit(); dit(); dit(); dah(); break;
      case 'w': dit(); dah(); dah(); break;
      case 'x': dah(); dit(); dit(); dah(); break;
      case 'y': dah(); dit(); dah(); dah(); break;
      case 'z': dah(); dah(); dit(); dit(); break;
      case '0': dah(); dah(); dah(); dah(); dah(); break;
      case '1': dit(); dah(); dah(); dah(); dah(); break;
      case '2': dit(); dit(); dah(); dah(); dah(); break;
      case '3': dit(); dit(); dit(); dah(); dah(); break;
      case '4': dit(); dit(); dit(); dit(); dah(); break;
      case '5': dit(); dit(); dit(); dit(); dit(); break;
      case '6': dah(); dit(); dit(); dit(); dit(); break;
      case '7': dah(); dah(); dit(); dit(); dit(); break;
      case '8': dah(); dah(); dah(); dit(); dit(); break;
      case '9': dah(); dah(); dah(); dah(); dit(); break;
      case '/': dah(); dit(); dit(); dah(); dit(); break;
      case '-': dah(); dit(); dit(); dit(); dit(); dah(); break;
      default: space();
    }
    end();
  }
  LowPower.sleep(60000);
}
