#! /bin/bash
#set -eu
#: $1

dir_video=../../data/movie1/
extension_video=mp4
dir_log=../../sample/out/30fps/
name_log=log.txt



if [ ! -e ${dir_log} ]; then
  mkdir -p ${dir_log}
fi

for file in `ls ${dir_video}*.${extension_video}`; do
    echo ${file}
    file2=${file#${dir_video}}
    #echo ${file2}
    file3=${file2%.${extension_video}}
    #echo ${file3}
    
    bash preprocess.sh ${dir_video} ${file3} ${extension_video} >> ${dir_log}${name_log}
    
done