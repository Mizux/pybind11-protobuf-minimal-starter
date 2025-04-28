include(FetchContent)
set(FETCHCONTENT_QUIET OFF)
set(FETCHCONTENT_UPDATES_DISCONNECTED ON)
set(BUILD_SHARED_LIBS OFF)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(BUILD_TESTING OFF)
set(CMAKE_Fortran_COMPILER OFF)

# ##############################################################################
# ABSEIL-CPP
# ##############################################################################
message(CHECK_START "Fetching Abseil-cpp")
list(APPEND CMAKE_MESSAGE_INDENT "  ")
set(ABSL_ENABLE_INSTALL ON)
set(ABSL_USE_SYSTEM_INCLUDES ON)
set(ABSL_PROPAGATE_CXX_STD ON)
set(ABSL_BUILD_TESTING OFF)
FetchContent_Declare(
  absl
  GIT_REPOSITORY "https://github.com/abseil/abseil-cpp.git"
  GIT_TAG "20250127.1"
  GIT_SHALLOW TRUE
  #PATCH_COMMAND git apply --ignore-whitespace
  #"${CMAKE_CURRENT_LIST_DIR}/../../patches/abseil-cpp-20250127.1.patch"
)
FetchContent_MakeAvailable(absl)
list(POP_BACK CMAKE_MESSAGE_INDENT)
message(CHECK_PASS "fetched")

# ##############################################################################
# Protobuf
# ##############################################################################
message(CHECK_START "Fetching Protobuf")
list(APPEND CMAKE_MESSAGE_INDENT "  ")
set(protobuf_BUILD_TESTS OFF)
set(protobuf_BUILD_SHARED_LIBS ON)
set(protobuf_BUILD_EXPORT OFF)
set(protobuf_MSVC_STATIC_RUNTIME OFF)
#set(protobuf_BUILD_LIBUPB ON)
FetchContent_Declare(
  Protobuf
  GIT_REPOSITORY "https://github.com/protocolbuffers/protobuf.git"
  GIT_TAG "v30.2"
  GIT_SHALLOW TRUE
  GIT_SUBMODULES ""
  #PATCH_COMMAND git apply --ignore-whitespace
  #"${CMAKE_CURRENT_LIST_DIR}/../../patches/protobuf-v30.2.patch"
)
FetchContent_MakeAvailable(Protobuf)
list(POP_BACK CMAKE_MESSAGE_INDENT)
message(CHECK_PASS "fetched")


# ##############################################################################
# Pybind11
# ##############################################################################
message(CHECK_START "Fetching pybind11")
list(APPEND CMAKE_MESSAGE_INDENT "  ")
set(PYBIND11_FINDPYTHON ON)
set(PYBIND11_INSTALL ON)
set(PYBIND11_TEST OFF)
FetchContent_Declare(
  pybind11
  GIT_REPOSITORY "https://github.com/pybind/pybind11.git"
  GIT_TAG "v2.13.6"
  GIT_SHALLOW TRUE
  PATCH_COMMAND git apply --ignore-whitespace
  "${CMAKE_CURRENT_LIST_DIR}/../../patches/pybind11-v2.13.6.patch"
)
FetchContent_MakeAvailable(pybind11)
list(POP_BACK CMAKE_MESSAGE_INDENT)
message(CHECK_PASS "fetched")

# ##############################################################################
# Pybind11 Protobuf
# ##############################################################################
message(CHECK_START "Fetching pybind11_protobuf")
list(APPEND CMAKE_MESSAGE_INDENT "  ")
FetchContent_Declare(
  pybind11_protobuf
  GIT_REPOSITORY "https://github.com/pybind/pybind11_protobuf.git"
  GIT_TAG "f02a2b7653bc50eb5119d125842a3870db95d251" # 2025/02/10
  #GIT_SHALLOW TRUE
  #PATCH_COMMAND git apply --ignore-whitespace
  #"${CMAKE_CURRENT_LIST_DIR}/../../patches/pybind11_protobuf.patch"
)
FetchContent_MakeAvailable(pybind11_protobuf)
list(POP_BACK CMAKE_MESSAGE_INDENT)
message(CHECK_PASS "fetched")
