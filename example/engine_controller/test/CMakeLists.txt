project(EngineControllerTest)

add_executable(${PROJECT_NAME}
    integration_test.cpp
)

target_link_libraries(${PROJECT_NAME}
    PUBLIC
        EngineController
)