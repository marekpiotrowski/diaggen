#include <engine_controller/engine_ecu.h>
#include <engine_controller/load_detector.h>
#include <engine_controller/temperature_sensor.h>

using namespace diaggen::engine_controller;

void testSettingThrottle()
{
    LoadDetector load_detector(1, 5);
    TemperatureSensor temperature_sensor;
    EngineEcu ecu(1, load_detector, temperature_sensor);
    ecu.setThrottle(78);
}

void testAdjustingToLoad()
{
    LoadDetector load_detector(1, 5);
    TemperatureSensor temperature_sensor;
    EngineEcu ecu(1, load_detector, temperature_sensor);
    ecu.adjustToCurrentLoad();
}

int main()
{
    testSettingThrottle();
    testAdjustingToLoad();
    return 0;
}