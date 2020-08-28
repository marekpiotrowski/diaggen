#ifndef ENGINE_CONTROLLER_API_ENGINE_CONTROLLER_ECU_H
#define ENGINE_CONTROLLER_API_ENGINE_CONTROLLER_ECU_H

#include <engine_controller/ecu.h>

namespace diaggen
{
namespace engine_controller
{

class Ecu
{
public:
    Ecu(int ecu_id);
    ~Ecu() = default;

    int getEcuId() const;
    void activate();
private:
    int ecu_id{0};
    bool is_on{false};
};

} // namespace engine_controller
} // namespace diaggen

#endif /* ENGINE_CONTROLLER_API_ENGINE_CONTROLLER_ECU_H */

