#include <iostream>

class AppNotFound{
    public:
        void error(){
            std::cout << "Could not determine name for app" << std::endl;
        }
};

extern "C" {
    AppNotFound* AppNotFound_new(){ return new AppNotFound(); }
    void AppNotFound_error(AppNotFound* error1){ error1->error(); }
}
