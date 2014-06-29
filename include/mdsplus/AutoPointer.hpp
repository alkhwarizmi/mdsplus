/*
 * AutoPointer.hpp
 *
 *  Created on: May 5, 2014
 *      Author: kerickso
 */

#ifndef MDS_AUTOPOINTER_HPP_
#define MDS_AUTOPOINTER_HPP_

#include <vector>
#include <string>

namespace MDSplus {

template<class T>
struct AutoPointer {
	AutoPointer(T * t): ptr(t) {
	}

	~AutoPointer() {
		delete ptr;
	}

	T * ptr;
};

template<>
struct AutoPointer<Data> {
	AutoPointer(Data * d): ptr(d) {
	}

	~AutoPointer() {
		deleteData(ptr);
	}

	Data * ptr;
};

template<class T>
struct AutoArray {
	AutoArray(T * t): ptr(t) {
	}

	virtual ~AutoArray() {
		delete[] ptr;
	}

	T * ptr;
};

template<class T>
struct AutoVector: public AutoArray<T> {
	AutoVector(T * vBeg, T* vEnd): AutoArray<T>(vBeg), vector(vBeg, vEnd) {}
	std::vector<T> vector;
};

struct AutoString: public AutoArray<char> {
	AutoString(char * cstr): AutoArray(cstr), string(cstr) {}
	std::string string;
};

}

#endif /* MDS_AUTOPOINTER_HPP_ */
