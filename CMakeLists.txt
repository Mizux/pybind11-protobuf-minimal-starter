cmake_minimum_required(VERSION 3.18)
project(Pybind11ProtobufMinimalStarter)

# Find Python 3
find_package(Python3 REQUIRED COMPONENTS Interpreter Development.Module)

# Build Needed dependencies
add_subdirectory(cmake/dependencies dependencies)

if(UNIX)
  option(BUILD_SHARED_LIBS "Build shared libraries (.so or .dylib)." ON)
endif()

# get_cpp_proto()
# CMake macro to generate Protobuf cpp sources
# Parameters:
#  the proto c++ headers list
#  the proto c++ sources list
# e.g.:
# get_cpp_proto(PROTO_HDRS PROTO_SRCS)
macro(get_cpp_proto PROTO_HDRS PROTO_SRCS)
  file(GLOB_RECURSE PROTO_FILES RELATIVE ${PROJECT_SOURCE_DIR} "example.proto")
  ## Get Protobuf include dir
  get_target_property(protobuf_dirs protobuf::libprotobuf INTERFACE_INCLUDE_DIRECTORIES)
  foreach(dir IN LISTS protobuf_dirs)
    if (NOT "${dir}" MATCHES "INSTALL_INTERFACE|-NOTFOUND")
      message(STATUS "protoc(cc) Adding proto path: ${dir}")
      list(APPEND PROTO_DIRS "--proto_path=${dir}")
    endif()
  endforeach()

  set(PROTOC_PRG protobuf::protoc)
  foreach(PROTO_FILE IN LISTS PROTO_FILES)
    message(STATUS "protoc(cc) .proto: ${PROTO_FILE}")
    get_filename_component(PROTO_DIR ${PROTO_FILE} DIRECTORY)
    get_filename_component(PROTO_NAME ${PROTO_FILE} NAME_WE)
    set(PROTO_HDR ${PROJECT_BINARY_DIR}/${PROTO_DIR}/${PROTO_NAME}.pb.h)
    set(PROTO_SRC ${PROJECT_BINARY_DIR}/${PROTO_DIR}/${PROTO_NAME}.pb.cc)
    message(STATUS "protoc(cc) hdr: ${PROTO_HDR}")
    message(STATUS "protoc(cc) src: ${PROTO_SRC}")
    add_custom_command(
      OUTPUT ${PROTO_SRC} ${PROTO_HDR}
      COMMAND ${PROTOC_PRG}
        "--proto_path=${PROJECT_SOURCE_DIR}"
        ${PROTO_DIRS}
        "--cpp_out=${PROJECT_BINARY_DIR}"
        ${PROTO_FILE}
      DEPENDS ${PROTO_NAME}.proto ${PROTOC_PRG}
      COMMENT "Generate C++ protocol buffer for ${PROTO_FILE}"
      WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}
      VERBATIM)
    list(APPEND ${PROTO_HDRS} ${PROTO_HDR})
    list(APPEND ${PROTO_SRCS} ${PROTO_SRC})
  endforeach()
endmacro()

add_library(helloworld)
get_cpp_proto(PROTO_HDRS PROTO_SRCS)
#message(FATAL_ERROR "${PROTO_HDRS}, ${PROTO_SRCS}")
target_sources(helloworld PRIVATE
  helloworld.h
  ${PROTO_SRCS} ${PROTO_HDRS}
)
target_include_directories(helloworld
  PUBLIC
    $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}>
    $<BUILD_INTERFACE:${PROJECT_BINARY_DIR}>
    $<INSTALL_INTERFACE:include>)
target_link_libraries(helloworld PUBLIC
  protobuf::libprotobuf
)

##############
##  Python  ##
##############
set(PROTO_PYS)
file(GLOB_RECURSE proto_py_files RELATIVE ${PROJECT_SOURCE_DIR} "example.proto")
## Get Protobuf include dir
get_target_property(protobuf_dirs protobuf::libprotobuf INTERFACE_INCLUDE_DIRECTORIES)
foreach(dir IN LISTS protobuf_dirs)
  if (NOT "${dir}" MATCHES "INSTALL_INTERFACE|-NOTFOUND")
    message(STATUS "protoc(cc) Adding proto path: ${dir}")
    list(APPEND PROTO_DIRS "--proto_path=${dir}")
  endif()
endforeach()
foreach(PROTO_FILE IN LISTS proto_py_files)
  message(STATUS "protoc(py) .proto: ${PROTO_FILE}")
  get_filename_component(PROTO_DIR ${PROTO_FILE} DIRECTORY)
  get_filename_component(PROTO_NAME ${PROTO_FILE} NAME_WE)
  set(PROTO_PY ${PROJECT_BINARY_DIR}/${PROTO_DIR}/${PROTO_NAME}_pb2.py)
  message(STATUS "protoc(py) py: ${PROTO_PY}")
  add_custom_command(
    OUTPUT ${PROTO_PY}
    COMMAND ${PROTOC_PRG}
    "--proto_path=${PROJECT_SOURCE_DIR}"
    ${PROTO_DIRS}
    "--python_out=${PROJECT_BINARY_DIR}"
    ${PROTO_FILE}
    DEPENDS ${PROTO_FILE} ${PROTOC_PRG}
    COMMENT "Generate Python 3 protocol buffer for ${PROTO_FILE}"
    WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}
    VERBATIM)
  list(APPEND PROTO_PYS ${PROTO_PY})
endforeach()
add_custom_target(helloworld_python_proto DEPENDS ${PROTO_PYS} helloworld)

pybind11_add_module(helloworld_pybind11 MODULE helloworld_pybind.cpp)
set_target_properties(helloworld_pybind11 PROPERTIES
  LIBRARY_OUTPUT_NAME "pyhelloworld")
# note: macOS is APPLE and also UNIX !
if(APPLE)
  set_target_properties(helloworld_pybind11 PROPERTIES
    SUFFIX ".so"
    INSTALL_RPATH "@loader_path;@loader_path/../lib"
  )
  set_property(TARGET helloworld_pybind11 APPEND PROPERTY
    LINK_FLAGS "-flat_namespace -undefined suppress"
  )
elseif(UNIX)
  set_target_properties(helloworld_pybind11 PROPERTIES
    INSTALL_RPATH "$ORIGIN:$ORIGIN/../lib"
  )
endif()
target_include_directories(helloworld_pybind11 PRIVATE
  ${protobuf_SOURCE_DIR})
target_link_libraries(helloworld_pybind11 PRIVATE
  helloworld
  pybind11_native_proto_caster)
add_dependencies(helloworld_pybind11 helloworld_python_proto)

# Disable CTest targets
set_property(GLOBAL PROPERTY CTEST_TARGETS_ADDED 1)
include(CTest)

configure_file(
  ${PROJECT_SOURCE_DIR}/pyhelloworld_test.py
  ${PROJECT_BINARY_DIR}/pyhelloworld_test.py
)
add_test(
  NAME pyhelloworld_test
  COMMAND ${Python3_EXECUTABLE} pyhelloworld_test.py
  WORKING_DIRECTORY ${PROJECT_BINARY_DIR}
)
