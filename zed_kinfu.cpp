#include <opencv2/opencv.hpp>
#include <opencv2/calib3d.hpp>
#include <opencv2/rgbd.hpp>
#include <opencv2/core.hpp>
#include <sl/Camera.hpp>
#include <iostream>

using namespace std;

int main(){
    
    // ZED camera setting
    sl::Camera zed;
    auto returned_state = zed.open();
    if (returned_state != sl::ERROR_CODE::SUCCESS) return 1;
    sl::Mat zed_image;
    
    // Opencv KinFu setting
    cv::Ptr<cv::kinfu::Params> params;
    params = cv::kinfu::Params::defaultParams();
    cv::Ptr<cv::kinfu::KinFu> kf;
    kf = cv::kinfu::KinFu::create(params);

    
    while(true){
        
        // ZED Mat -> CV Mat
        zed.grab();
        zed.retrieveImage(zed_image, sl::VIEW::DEPTH);
        cv::Mat cvImage = cv::Mat((int)zed_image.getHeight(), (int)zed_image.getWidth(), CV_8UC4, zed_image.getPtr<sl::uchar1>(sl::MEM::CPU));
        cv::resize(cvImage, cvImage, cv::Size(640, 480));
        cv::cvtColor(cvImage, cvImage, cv::COLOR_BGR2GRAY);
        
        // Updata KinectFusion
        kf->update(cvImage);
        kf->render(tsdfRender);

        // imshow
        cv::imshow("Depth", cvImage);
        cv::imshow("Render", tsdfRender);
        if (cv::waitKey(10) == 'q') break;
    }

    cv::destroyAllWindows();
    zed.close();

    return 0;
}