#ifndef ENGINE_CONTROLLER_API_ENGINE_CONTROLLER_TEMPERATURE_SENSOR_H
#define ENGINE_CONTROLLER_API_ENGINE_CONTROLLER_TEMPERATURE_SENSOR_H

#include <engine_controller/ecu.h>

namespace diaggen
{
namespace engine_controller
{

class TemperatureSensor
{
public:
    TemperatureSensor() = default;
    ~TemperatureSensor() = default;

    double isTemperatureOk() const;
    double isIncreasing() const;

    void reset();

    constexpr static int HISTORICAL_SAMPLES_COUNT = 15;
private:
    std::array<double, HISTORICAL_SAMPLES_COUNT> previous_temperatures_;
};

} // namespace engine_controller
} // namespace diaggen

#endif /* ENGINE_CONTROLLER_API_ENGINE_CONTROLLER_TEMPERATURE_SENSOR_H */

