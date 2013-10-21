#ifndef MDSTYPES_H
#define MDSTYPES_H

#ifndef HAVE_VXWORKS_H
#include <config.h>
#endif

#ifdef HAVE_STDINT_H
#include <stdint.h>
typedef int64_t _int64;
typedef uint64_t _int64u;
#else
#ifdef HAVE_WINDOWS_H
#include <msc_stdint.h>
typedef unsigned __int64 _int64u;
#else

#ifdef HAVE_VXWORKS_H
typedef long long _int64;
typedef unsigned long long _int64u;
typedef int intptr_t
#else

#if (SIZEOF__INT64 != 8)
#if (SIZEOF_LONG == 8)
typedef long _int64;
typedef unsigned long _int64u;
#elif (SIZEOF_LONG_LONG == 8)
typedef long long _int64;
typedef unsigned long long _int64u;
#endif
#else
typedef unsigned _int64 _int64u;
#endif
#endif
typedef  _int64 int64_t
typedef  _int64u uint64_t
#endif /*vxWorks*/
#endif
#endif
