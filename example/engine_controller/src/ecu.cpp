#include <engine_controller/ecu.h>

namespace diaggen
{
namespace engine_controller
{

Ecu::Ecu(int ecu_id) : ecu_id_(ecu_id) {}

int Ecu::getEcuId() const
{
    return ecu_id_;
}

void Ecu::activate()
{
    is_on_ = true;
}

} // namespace engine_controller
} // namespace diaggen
