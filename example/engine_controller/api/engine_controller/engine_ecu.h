#ifndef ENGINE_CONTROLLER_API_ENGINE_CONTROLLER_ENGINE_ECU_H
#define ENGINE_CONTROLLER_API_ENGINE_CONTROLLER_ENGINE_ECU_H

#include <engine_controller/ecu.h>

namespace diaggen
{
namespace engine_controller
{

class EngineEcu : public Ecu
{
public:
    EngineEcu(int ecu_id);
    ~EngineEcu() = default;

    double setThrottle();
    bool canIncreaseThrottle() const;
    void adjustToCurrentLoad();
private:
    LoadDetector detector_;
    TemperatureSensor temperature_sensor_;
};

} // namespace engine_controller
} // namespace diaggen

#endif /* ENGINE_CONTROLLER_API_ENGINE_CONTROLLER_ENGINE_ECU_H */

