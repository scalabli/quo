#include <iostream>

class AppNotFound{
	public:
	       	void app_error(){
		       	std::cout << "Could not determine name for app" << std::endl;
        }
};


extern "C" {
    AppNotFound* AppNotFound_new(){ return new AppNotFound(); }
    void AppNotFound_app_error(AppNotFound* appnotfound){ appnotfound->app_error(); }
}
