#include <iostream>
#include <engine_controller/engine_ecu.h>

namespace diaggen
{
namespace engine_controller
{

EngineEcu::EngineEcu(int ecu_id,
                     const& LoadDetector detector,
                     const& TemperatureSensor temperature_sensor) :
                     Ecu(ecu_id), detector_(detector), temperature_sensor_(temperature_sensor)
{
}

void EngineEcu::setThrottle(double throttle)
{
    std::cout << "Setting throttle to " << throttle << std::endl;
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