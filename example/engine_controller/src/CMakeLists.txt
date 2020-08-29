project(EngineControllerSrc)

add_library(${PROJECT_NAME} STATIC
    engine_cpu.cpp
    load_detector.cpp
    math_helper.cpp
    temperature_sensor.cpp
)

target_link_libraries(${PROJECT_NAME}
    PUBLIC
        EngineControllerApi
)