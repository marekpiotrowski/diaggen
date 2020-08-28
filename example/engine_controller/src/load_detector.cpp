#include <vector>
#include <engine_controller/load_detector.h>

namespace diaggen
{
namespace engine_controller
{

LoadDetector::LoadDetector(double min_allowable_load, double max_allowable_load) :
    min_allowable_load_(min_allowable_load), max_allowable_load_(max_allowable_load)
{
}

bool LoadDetector::isStatusOk() const
{
    return current_load_ < max_allowable_load_ && current_load_ > min_allowable_load;
}

bool LoadDetector::isDecreasing() const
{
    double previous_load = 1e10;
    for(const auto& load : previous_loads_)
    {
        if(load > previous_load)
        {
            return false;
        }
        previous_load = load;
    }
    return true;
}

void LoadDetector::adjustAllowableLoads(double min_allowable_load, double max_allowable_load)
{
    min_allowable_load_ = min_allowable_load;
    max_allowable_load_ = max_allowable_load;
}

void LoadDetector::refreshReading()
{
    previous_loads_ = std::vector<double>();
    for(double i = 5; i > 2; i -= 0.3)
    {
        previous_loads_.push_back(i);
    }
    current_load_ = *(previous_loads_.back());
}

} // namespace engine_controller
} // namespace diaggen