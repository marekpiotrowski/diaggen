#ifndef ENGINE_CONTROLLER_API_ENGINE_CONTROLLER_LOAD_DETECTOR_H
#define ENGINE_CONTROLLER_API_ENGINE_CONTROLLER_LOAD_DETECTOR_H

#include <vector>

namespace diaggen
{
namespace engine_controller
{

class LoadDetector
{
public:
    LoadDetector(double min_allowable_load, double max_allowable_load);
    ~LoadDetector() = default;

    double isStatusOk() const;
    double isDecreasing() const;
    void adjustAllowableLoads(double min_allowable_load, double max_allowable_load);
    void refreshReading();
private:
    double min_allowable_load_;
    double max_allowable_load_;
    double current_load_{0};
    std::vector<double> previous_loads_;
};

} // namespace engine_controller
} // namespace diaggen

#endif /* ENGINE_CONTROLLER_API_ENGINE_CONTROLLER_LOAD_DETECTOR_H */

