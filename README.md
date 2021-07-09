# Video Feature Extraction
This repository is a compilation of video feature extractor code.  
The base technique is here and has been rewritten for your own use.  
The procedure for execution is described.  

About code that needs to be edited  
## preprocess.sh
As a premise, use FFmpeg to cut out the frame from the video.  
Please refer to this as there is a reference article (example).  
### 1.settings
(1) CONVERT_VIDEO_TO_IMG: true or false  
(2) CROP_VIDEO: true or false  
(3) RUN_I3D_PYTORCH: true (fixed)  

### 2.video information
(1) frame_rate: Match the frame rate of the video  
(2) dir_image: Output destination of the cut-out image  
(3) name_image: Give a serial number to the cut-out image  
(4) extension_image: Specify the extension of the cut-out image  

    optional information
    (1) start_time_sec: Start position of cutting  
    (2) continuous_time_sec: Cutout time range (If you set a large value, it will cut out to the end.)  
    (3) mode: RGB or flow  
    (4) load_model: Reference model (default-> rgb_charades.pt)  
    (5) root: Directory with images  
    (6) save_dir: Save destination of extracted features  

## run_preprocess.sh
(1) dir_video: Directory with the video you want to extract  
(2) extension_video: Video extension  
(3) dir_log: Specify the output destination of log.txt that records the progress of extraction  
(4) name_log: log.txt (fixed)  
