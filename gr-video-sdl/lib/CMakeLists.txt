# Copyright 2011,2012 Free Software Foundation, Inc.
#
# This file is part of GNU Radio
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

if(UNIX)
#    add_compile_options( $<$<CONFIG:Debug>:-g3 -O0> )
    add_compile_options( -fPIC -flto=auto)
    if( CMAKE_BUILD_TYPE STREQUAL Debug )
        add_compile_options( -g3 -O0)
    endif()
elseif(WIN32)
    add_compile_definitions("BOOST_USE_WINAPI_VERSION=0x0602")
    add_compile_definitions("_WIN32_WINNT=0x0602")
    add_compile_definitions("BOOST_PROCESS_VERSION=2")
    string(REPLACE "/O2" "/Od" CMAKE_CXX_FLAGS_RELWITHDEBINFO ${CMAKE_CXX_FLAGS_RELWITHDEBINFO})
    string(REPLACE "/Ob1" "/Ob0" CMAKE_CXX_FLAGS_RELWITHDEBINFO ${CMAKE_CXX_FLAGS_RELWITHDEBINFO})
endif()


########################################################################
# Setup library
########################################################################
add_library(gnuradio-video-sdl sink_s_impl.cc sink_uc_impl.cc)

#find_package(Boost CONFIG REQUIRED COMPONENTS thread)

target_link_libraries(
    gnuradio-video-sdl
    PUBLIC gnuradio-runtime
    PRIVATE ${SDL_LIBRARY})

if(0)
    target_link_libraries(gnuradio-video-sdl PRIVATE common-precompiled-headers)
endif()

target_include_directories(
    gnuradio-video-sdl
    PUBLIC $<INSTALL_INTERFACE:include>
           $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/../include> ${SDL_INCLUDE_DIR})

#Add Windows DLL resource file if using MSVC
if(MSVC)
    include(${PROJECT_SOURCE_DIR}/cmake/Modules/GrVersion.cmake)

    configure_file(${CMAKE_CURRENT_SOURCE_DIR}/gnuradio-video-sdl.rc.in
                   ${CMAKE_CURRENT_BINARY_DIR}/gnuradio-video-sdl.rc @ONLY)

    target_sources(gnuradio-video-sdl
                   PRIVATE ${CMAKE_CURRENT_BINARY_DIR}/gnuradio-video-sdl.rc)
endif(MSVC)

if(BUILD_SHARED_LIBS)
    gr_library_foo(gnuradio-video-sdl)
endif()
