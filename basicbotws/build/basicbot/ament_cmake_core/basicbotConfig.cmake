# generated from ament/cmake/core/templates/nameConfig.cmake.in

# prevent multiple inclusion
if(_basicbot_CONFIG_INCLUDED)
  # ensure to keep the found flag the same
  if(NOT DEFINED basicbot_FOUND)
    # explicitly set it to FALSE, otherwise CMake will set it to TRUE
    set(basicbot_FOUND FALSE)
  elseif(NOT basicbot_FOUND)
    # use separate condition to avoid uninitialized variable warning
    set(basicbot_FOUND FALSE)
  endif()
  return()
endif()
set(_basicbot_CONFIG_INCLUDED TRUE)

# output package information
if(NOT basicbot_FIND_QUIETLY)
  message(STATUS "Found basicbot: 0.0.0 (${basicbot_DIR})")
endif()

# warn when using a deprecated package
if(NOT "" STREQUAL "")
  set(_msg "Package 'basicbot' is deprecated")
  # append custom deprecation text if available
  if(NOT "" STREQUAL "TRUE")
    set(_msg "${_msg} ()")
  endif()
  # optionally quiet the deprecation message
  if(NOT basicbot_DEPRECATED_QUIET)
    message(DEPRECATION "${_msg}")
  endif()
endif()

# flag package as ament-based to distinguish it after being find_package()-ed
set(basicbot_FOUND_AMENT_PACKAGE TRUE)

# include all config extra files
set(_extras "")
foreach(_extra ${_extras})
  include("${basicbot_DIR}/${_extra}")
endforeach()
