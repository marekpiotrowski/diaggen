#include <iostream>
#include <chrono>
#include <thread>
#include <engine_controller/engine_ecu.h>

namespace diaggen
{
namespace engine_controller
{

EngineEcu::EngineEcu(int ecu_id, const LoadDetector& detector, const TemperatureSensor& temperature_sensor) :
                     Ecu(ecu_id), detector_(detector), temperature_sensor_(temperature_sensor)
{
}

void EngineEcu::setThrottle(double throttle)
{
    using namespace std::chrono_literals;
    if(!canIncreaseThrottle()) {
        temperature_sensor_.reset();
        detector_.refreshReading();
    } else
    {
        detector_.adjustAllowableLoads(11, 12);
    }
    std::this_thread::sleep_for(1s);
    if(temperature_sensor_.isTemperatureOk())
    {
        std::cout << "Setting throttle to " << throttle << std::endl;
    }
    std::cout << "Setting throttle failed!" << std::endl;
}

bool EngineEcu::canIncreaseThrottle() const
{
    return (!temperature_sensor_.isIncreasing() && detector_.isStatusOk());
}

void EngineEcu::adjustToCurrentLoad()
{
    detector_.adjustAllowableLoads(1.0, 3.0);
}

} // namespace engine_controller
} // namespace diaggen