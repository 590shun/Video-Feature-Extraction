#! /bin/bash
#set -eu
#: $1

#1: convert video to continuous image by ffmpeg
#2: extract features

#----- settings -----
#1-1
CONVERT_VIDEO_TO_JPG=true
#1-2
CROP_VIDEO=true

#2-1
RUN_I3D_PYTORCH=true

#----- video information -----
dir_in_video=$1
name_video=$2
extension_video=$3

frame_rate=30

dir_image=../sample/out/${name_video}/
name_image=%06d
extension_image=.jpg

#----- optional information #1-2 -----
start_time_sec=0
continuous_time_sec=1000 # temporary

#----- optional information #2-1 -----
mode=rgb
load_model=./models/rgb_charades.pt
root=../../data/sample/out/30fps/
save_dir=../../data/sample/out/
name_file=${name_video}


#----- main -----
if [ ! -e ${dir_image}]; then
  mkdir -p ${dir_image}
fi

#1
if ${CONVERT_VIDEO_TO_JPG}; then
  echo "Converting video to JPG from ${name_video}.${extension_video} ..."
  if ${CROP_VIDEO}; then
    ffmpeg -i ${dir_video}${name_video}.${extension_video} -ss ${start_time_sec} -t ${continuous_time_sec} -f image2 -vcodec mjpeg -qscale 1 -qmin 1 -qmax 1 -r ${frame_rate} ${dir_image}${name_image}${extension_image}
  else
    ffmpeg -i ${dir_video}${name_video}.${extension_video} -f image2 -vcodec mjpeg -qscale 1 -qmin 1 -qmax 1 -r ${frame_rate} ${dir_image}${name_image}${extension_image}
  fi
fi

num_of_file=$(ls "${dir_image}" | wc -w)
echo "Num of file : ${num_of_file}"

#2
if ${RUN_I3D_PYTORCH}; then
  echo "Running pytorch I3D to extract features ..."
  if [ ! -e ${save_dir} ]; then
    mkdir -p ${save_dir}
  fi
  python extract_features.py -mode ${mode} -load_model ${load_model} -root ${root} -save_dir ${save_dir} -file ${name_file}
fi


echo "All Finished"
