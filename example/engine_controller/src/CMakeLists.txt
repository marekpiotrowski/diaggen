project(EngineController)

add_library(${PROJECT_NAME} STATIC
    engine_ecu.cpp
    load_detector.cpp
    math_helper.cpp
    temperature_sensor.cpp
    ecu.cpp
)

target_link_libraries(${PROJECT_NAME}
    PUBLIC
        EngineControllerApi
)