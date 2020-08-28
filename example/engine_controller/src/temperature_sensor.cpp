#include <array>

#include <engine_controller/temperature_sensor.h>
#include "math_helper.h"

namespace diaggen
{
namespace engine_controller
{

bool TemperatureSensor::isTemperatureOk() const
{
    return math::toCelsius(*previous_temperatures_.back()) < 90;
}
bool TemperatureSensor::isIncreasing() const
{
    double previous_temperature = -1e10;
    for(const auto& temperature : previous_temperatures_)
    {
        if(temperature < previous_temperature)
        {
            return false;
        }
        previous_temperature = temperature;
    }
    return true;
}

void TemperatureSensor::refreshReadings()
{
    previous_loads_ = std::vector<double>();
    for(int i = 0; i < previous_temperatures_.size(); i++)
    {
        previous_temperatures_[i] = 88;
    }
}

void TemperatureSensor::reset()
{
    previous_temperatures_ = std::array<double, HISTORICAL_SAMPLES_COUNT>();
}

} // namespace engine_controller
} // namespace diaggen