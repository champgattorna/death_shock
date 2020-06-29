/* Necessary code for the arduino to communicate with Python code
 * Pretty simple stuff, reads in data from Python as a String and
 * parses it into an int. If true, sends a signal on pin 3 which
 * is connected to the relay which is hooked up to the TENS unit
 * 
 * Christian Hamp-Gattorna 2020
 */
void setup() {
  Serial.begin(9600);
  Serial.setTimeout(10);
  pinMode(3, OUTPUT);

}
void loop() {
  if(Serial.available() > 0) {
    String data = Serial.readString();
    int datanum = data.toInt();
    if(datanum == 1) {
      digitalWrite(3, HIGH);
      delay(1000);
      digitalWrite(3, LOW);
    }
  }
}
