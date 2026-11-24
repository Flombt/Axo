#include <Arduino.h>
#include <EEPROM.h>
#include <Servo.h>
#include <ctype.h>
#include <stddef.h>
#include <stdlib.h>
#include <string.h>

constexpr uint8_t AXES = 4;
constexpr uint8_t BUTTON = 2;
constexpr uint16_t LOW_US = 800, HIGH_US = 2200;
constexpr uint16_t HOLD_MS = 2000, DEBOUNCE_MS = 35, FRAME_MS = 20;
constexpr uint8_t STEP_US = 2, DEMO_FRACTION = 25;
constexpr uint16_t MAGIC = 0xA009;

const uint8_t pins[AXES] = {3, 5, 6, 9};
const char* const axes[AXES] = {"J2", "J3", "J7", "T1"};
struct Range {
  uint16_t low;
  uint16_t home;
  uint16_t high;
  int8_t direction;
};
struct Record {
  uint16_t magic;
  Range range[AXES];
  uint16_t check;
};
enum class Mode : uint8_t { Idle, Bench, Armed, Move };

Servo servos[AXES];
Record setupData = {};
Mode mode = Mode::Idle;
uint16_t sent[AXES] = {};
uint8_t axisInMotion = 0;
bool returning = false;
uint16_t goal = 0;
uint32_t lastFrame = 0, rawSince = 0, pressSince = 0;
bool rawDown = false, down = false, consumed = false, buttonReady = false;
char line[52];
uint8_t used = 0;
bool overlong = false;

uint16_t checksum() {
  uint16_t sum = 0x34a7;
  const uint8_t* p = reinterpret_cast<const uint8_t*>(&setupData);
  for (size_t i = 0; i < offsetof(Record, check); i++) {
    sum = (sum * 31u) ^ p[i];
  }
  return sum;
}

bool valid(const Range& r) {
  return r.low >= LOW_US && r.low < r.home && r.home < r.high &&
         r.high <= HIGH_US && (r.direction == 1 || r.direction == -1);
}

bool allValid() {
  for (const auto& r : setupData.range) {
    if (!valid(r)) return false;
  }
  return true;
}

void stop() {
  for (auto& motor : servos) motor.detach();
  mode = Mode::Idle;
  Serial.println(F("STOP PWM. Soutenir le bras et couper le 5 V moteurs."));
}

void engage(uint8_t axis, uint16_t us) {
  servos[axis].writeMicroseconds(us);
  servos[axis].attach(pins[axis], LOW_US, HIGH_US);
  sent[axis] = us;
}

uint16_t demoGoal(uint8_t axis) {
  const auto& r = setupData.range[axis];
  if (r.direction > 0) return r.home + ((r.high - r.home) * DEMO_FRACTION) / 100;
  return r.home - ((r.home - r.low) * DEMO_FRACTION) / 100;
}

void beginGesture() {
  axisInMotion = 0;
  goal = demoGoal(axisInMotion);
  returning = false;
  mode = Mode::Move;
  Serial.println(F("Cycle a vide."));
}

void runMotor(uint32_t now) {
  if (mode != Mode::Bench && mode != Mode::Move) return;
  if (now - lastFrame < FRAME_MS) return;
  lastFrame = now;
  uint16_t& value = sent[axisInMotion];
  if (value != goal) {
    value = value < goal ? min(uint16_t(value + STEP_US), goal) :
                          max(uint16_t(value - STEP_US), goal);
    servos[axisInMotion].writeMicroseconds(value);
    return;
  }
  if (mode == Mode::Bench) return;
  if (!returning) {
    returning = true;
    goal = setupData.range[axisInMotion].home;
    return;
  }
  if (++axisInMotion == AXES) {
    mode = Mode::Armed;
    Serial.println(F("Cycle termine. HOME tenu. STOP ou couper avec le bras soutenu."));
    return;
  }
  returning = false;
  goal = demoGoal(axisInMotion);
}

void checkButton(uint32_t now) {
  bool sampled = digitalRead(BUTTON) == LOW;
  if (sampled != rawDown) {
    rawDown = sampled;
    rawSince = now;
  }
  if (!buttonReady) {
    if (!rawDown && now - rawSince >= DEBOUNCE_MS) buttonReady = true;
    return;
  }
  if (rawDown != down && now - rawSince >= DEBOUNCE_MS) {
    down = rawDown;
    if (down) {
      pressSince = now;
      consumed = mode == Mode::Move || mode == Mode::Bench;
      if (consumed) stop();
    } else if (!consumed && mode == Mode::Armed && now - pressSince < HOLD_MS) {
      beginGesture();
    }
  }
  if (!down || consumed || now - pressSince < HOLD_MS) return;
  consumed = true;
  if (mode == Mode::Armed) {
    stop();
  } else if (mode == Mode::Idle && allValid()) {
    for (uint8_t i = 0; i < AXES; i++) engage(i, setupData.range[i].home);
    mode = Mode::Armed;
    Serial.println(F("HOME active. Appui bref pour le cycle, appui long pour STOP."));
  } else {
    Serial.println(F("Calibration incomplete."));
  }
}

int axisNumber(const char* value) {
  if (value) {
    for (uint8_t i = 0; i < AXES; i++) {
      if (strcmp(value, axes[i]) == 0) return i;
    }
  }
  return -1;
}

uint16_t pulse(const char* value) {
  if (!value || strlen(value) != 4) return 0;
  for (uint8_t i = 0; i < 4; i++) if (!isdigit(value[i])) return 0;
  return static_cast<uint16_t>(atoi(value));
}

void info() {
  for (uint8_t i = 0; i < AXES; i++) {
    Serial.print(axes[i]); Serial.print(F(" D")); Serial.print(pins[i]);
    const auto& r = setupData.range[i];
    if (valid(r)) {
      Serial.print(F("  ")); Serial.print(r.low); Serial.print(' ');
      Serial.print(r.home); Serial.print(' '); Serial.print(r.high);
      Serial.println(r.direction > 0 ? F(" +") : F(" -"));
    } else {
      Serial.println(F("  a calibrer"));
    }
  }
  Serial.println(F("INFO | TEST <axe> <us> | CAL <axe> <min> <home> <max> <+|-> | SAVE | STOP"));
}

void command(char* buffer) {
  const char* op = strtok(buffer, " \t");
  if (!op) return;
  if (!strcmp(op, "STOP")) {
    stop();
  } else if (!strcmp(op, "INFO")) {
    info();
  } else if (!strcmp(op, "SAVE") && mode == Mode::Idle && allValid()) {
    setupData.magic = MAGIC;
    setupData.check = checksum();
    EEPROM.put(0, setupData);
    Serial.println(F("Calibration en EEPROM."));
  } else if (!strcmp(op, "CAL") && mode == Mode::Idle) {
    int axis = axisNumber(strtok(nullptr, " \t"));
    Range r = {};
    r.low = pulse(strtok(nullptr, " \t"));
    r.home = pulse(strtok(nullptr, " \t"));
    r.high = pulse(strtok(nullptr, " \t"));
    const char* dir = strtok(nullptr, " \t");
    if (dir && !strcmp(dir,"+")) r.direction = 1;
    if (dir && !strcmp(dir,"-")) r.direction = -1;
    if (axis < 0 || !valid(r) || strtok(nullptr, " \t")) {
      Serial.println(F("CAL refuse. / INFO"));
      return;
    }
    setupData.range[axis] = r;
    Serial.println(F("Calibration en RAM."));
  } else if (!strcmp(op, "TEST") && (mode == Mode::Idle || mode == Mode::Bench)) {
    int axis = axisNumber(strtok(nullptr, " \t"));
    uint16_t us = pulse(strtok(nullptr, " \t"));
    if (axis < 0 || us < LOW_US || us > HIGH_US || strtok(nullptr, " \t") ||
        (mode == Mode::Bench && axis != axisInMotion)) {
      Serial.println(F("TEST refuse. STOP avant de changer de moteur."));
      return;
    }
    if (mode == Mode::Idle) {
      if (us != 1500) {
        Serial.println(F("Premier TEST a 1500 us, palonnier debraye et axe libre."));
        return;
      }
      axisInMotion = axis;
      engage(axis, us);
      mode = Mode::Bench;
    }
    goal = us;
    Serial.println(F("TEST en cours."));
  } else {
    Serial.println(F("Commande refusee. INFO ou STOP."));
  }
}

void setup() {
  pinMode(BUTTON, INPUT_PULLUP);
  rawDown = digitalRead(BUTTON) == LOW;
  rawSince = millis();
  Serial.begin(115200);
  EEPROM.get(0, setupData);
  if (setupData.magic != MAGIC || setupData.check != checksum() || !allValid()) {
    memset(&setupData, 0, sizeof(setupData));
  }
  Serial.println(F("AURA-009 r02 / PWM inactif."));
  info();
}

void loop() {
  uint32_t now = millis();
  checkButton(now);
  runMotor(now);
  while (Serial.available()) {
    char ch = Serial.read();
    if (ch == '\n' || ch == '\r') {
      line[used] = '\0';
      if (!overlong && used) command(line);
      else if (overlong) Serial.println(F("Ligne trop longue."));
      used = 0;
      overlong = false;
    } else if (used < sizeof(line)-1) {
      line[used++] = ch;
    } else {
      overlong = true;
    }
  }
}
