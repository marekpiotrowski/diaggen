#ifndef ENGINE_CONTROLLER_API_ENGINE_CONTROLLER_TEMPERATURE_SENSOR_H
#define ENGINE_CONTROLLER_API_ENGINE_CONTROLLER_TEMPERATURE_SENSOR_H

#include <array>
#include <engine_controller/temperature_sensor.h>

namespace diaggen
{
namespace engine_controller
{

class TemperatureSensor
{
public:
    TemperatureSensor() = default;
    ~TemperatureSensor() = default;

    bool isTemperatureOk() const;
    bool isIncreasing() const;

    void refreshReadings();

    void reset();

    constexpr static int HISTORICAL_SAMPLES_COUNT = 15;
private:
    std::array<double, HISTORICAL_SAMPLES_COUNT> previous_temperatures_;
};

} // namespace engine_controller
} // namespace diaggen

#endif /* ENGINE_CONTROLLER_API_ENGINE_CONTROLLER_TEMPERATURE_SENSOR_H */

