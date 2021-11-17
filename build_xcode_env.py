import argparse
import os
import subprocess

def get_cmake_file(project_name: str) -> str:

    cmake_list_txt = f'''cmake_minimum_required(VERSION 3.2 FATAL_ERROR)

set (CMAKE_CXX_STANDARD 11)
project({project_name})
    
find_package(OpenCV 4.0.1 REQUIRED)
    
include_directories(${{OpenCV_INCLUDE_DIRS}})
file(GLOB SOURCES *.cpp)
    
add_executable ({project_name} ${{SOURCES}})
target_link_libraries ({project_name}
PRIVATE ${{OpenCV_LIBS}}
)
'''
    return cmake_list_txt

def get_cpp_file_template() -> str:

    cpp_file_template = f'''
#include <stdio.h>
#include <iostream>
#include <opencv2/opencv.hpp>
#define FILENAME ""
int main(int argc, const char * argv[]) {{
    cv::Mat src_img = cv::imread(FILENAME, 0);
    if (src_img.empty()) {{
        return (-1);
    }}

    cv::imshow("input", src_img);
    cv::imshow("binary", bin_img);cv::waitKey();
    return 0;
}}
'''
    return cpp_file_template

def main():

    parser = argparse.ArgumentParser(description='create xcode builder.')
    parser.add_argument('p', help='project name')
    args = parser.parse_args()

    project_name = args.p

    cmake_list_txt = get_cmake_file(project_name)

    # write cmakelist.txt
    os.makedirs(f'./{project_name}', exist_ok=True)
    dir_path = f'./{project_name}'
    cmake_file_name = 'CMakeLists.txt'
    cmake_file_path = os.path.join(dir_path, cmake_file_name)
    with open(cmake_file_path, mode='w') as f:
        f.write(cmake_list_txt)

    cpp_template = get_cpp_file_template()
    cpp_file_name = f'{project_name}.cpp'
    cpp_file_path = os.path.join(dir_path, cpp_file_name)

    with open(cpp_file_path, mode='w') as f:
        f.write(cpp_file_name)

    # build xcode
    command = 'cmake ./ -G Xcode'
    os.chdir(dir_path)
    subprocess.call(command, shell=True)

if __name__ == '__main__':
    main()