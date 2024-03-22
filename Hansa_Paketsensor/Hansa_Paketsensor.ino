#include <EEPROM.h>

#define EEPROM_VALUE_ADDR 1
#define passPhrase "request-connect"
#define kalibMode "kalibrieren"
#define DatapointsPerSecond 50
#define shunt 0.220              //kilo Ohm

float voltage = 0;
float ampere = 0;
float counts = 0;
bool serConnected = false;


void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(A0, INPUT);
  Serial.begin(9600);
  digitalWrite(LED_BUILTIN, HIGH);
}


float readKw() {
  float gelesen;
  EEPROM.get(EEPROM_VALUE_ADDR, gelesen);
  return gelesen;
}


float writeKw(float geschrieben) {
  EEPROM.put(EEPROM_VALUE_ADDR, geschrieben);
  float gelesen = readKw();
  Serial.println(String(gelesen));
}


long readVcc() {
  long result;
  // Read 1.1V reference against AVcc
#if defined(__AVR_ATmega32U4__) || defined(__AVR_ATmega1280__) || defined(__AVR_ATmega2560__)
  ADMUX = _BV(REFS0) | _BV(MUX4) | _BV(MUX3) | _BV(MUX2) | _BV(MUX1);
#elif defined (__AVR_ATtiny24__) || defined(__AVR_ATtiny44__) || defined(__AVR_ATtiny84__)
  ADMUX = _BV(MUX5) | _BV(MUX0);
#elif defined (__AVR_ATtiny25__) || defined(__AVR_ATtiny45__) || defined(__AVR_ATtiny85__)
  ADMUX = _BV(MUX3) | _BV(MUX2);
#else
  ADMUX = _BV(REFS0) | _BV(MUX3) | _BV(MUX2) | _BV(MUX1);
#endif
  delay(2); // Wait for Vref to settle
  ADCSRA |= _BV(ADSC); // Convert
  while (bit_is_set(ADCSRA, ADSC));
  result = ADCL;
  result |= ADCH << 8;
  result = 1126400L / result; // Calculate Vcc (in mV); 1126400 = 1.1*1024*1000
  return result;
}


void loop() {

  //warten bis Serielle Schnittstelle sichergestellt ist
  while (serConnected == false) {
    String SerIncoming = Serial.readString();

    //wert vom kalibrieren speichern
    if (SerIncoming.equals(kalibMode)) {
      Serial.println("Kalibrieren");
      Serial.println("Bitte Wert eingeben");
      //warten auf werteingabe
      while (Serial.available() == 0) {
      }
      float kalibIn = Serial.parseFloat();
      writeKw(kalibIn);
    } else if (SerIncoming.equals(passPhrase)) {
      Serial.println("connection established");
      Serial.println(String(readKw()));
      serConnected = true;
      digitalWrite(LED_BUILTIN, LOW);
      delay(200);
      break;
    }
  }

  counts = analogRead(A0);

  voltage = counts * (readVcc() / 10.24);   //1/100 V
  voltage /= 100;                           //milli volt
  ampere = voltage / shunt;
  Serial.println(ampere);                   //micro amper
  //warten
  delay(1000 / DatapointsPerSecond);

}
