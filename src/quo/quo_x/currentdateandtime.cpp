// CPP program to print current date and time
// using chronos.
#include <chrono>
#include <ctime>
#include <iostream>

using namespace std;
class DateTime{
	public:
		void datetime(){
			auto timenow =  chrono::system_clock::to_time_t(chrono::system_clock::now());
			cout << ctime(&timenow) << endl;

}
};

extern "C" {
    DateTime* DateTime_new(){ return new DateTime(); }
    void DateTime_datetime(DateTime* currentdateandtime){ currentdateandtime->datetime(); }
}
