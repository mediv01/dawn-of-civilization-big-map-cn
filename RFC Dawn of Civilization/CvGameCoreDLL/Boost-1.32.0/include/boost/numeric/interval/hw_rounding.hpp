/* Boost interval/hw_rounding.hpp template implementation file
 *
 * Copyright 2002 Herv? Br?nnimann, Guillaume Melquiond, Sylvain Pion
 *
 * Distributed under the Boost Software License, Version 1.0.
 * (See accompanying file LICENSE_1_0.txt or
 * copy at http://www.boost.org/LICENSE_1_0.txt)
 */

#ifndef BOOST_NUMERIC_INTERVAL_HW_ROUNDING_HPP
#define BOOST_NUMERIC_INTERVAL_HW_ROUNDING_HPP

#include <boost/numeric/interval/rounding.hpp>
#include <boost/numeric/interval/rounded_arith.hpp>

// define appropriate specialization of rounding_control for built-in types
#if defined(__i386__) || defined(_M_IX86) || defined(__BORLANDC__)
#  include <boost/numeric/interval/detail/x86_rounding_control.hpp>
#elif defined(powerpc) || defined(__powerpc__) || defined(__ppc__)
#  include <boost/numeric/interval/detail/ppc_rounding_control.hpp>
#elif defined(sparc) || defined(__sparc__)
#  include <boost/numeric/interval/detail/sparc_rounding_control.hpp>
#elif defined(__USE_ISOC99)
#  include <boost/numeric/interval/detail/c99_rounding_control.hpp>
#else
#  error Boost.Numeric.Interval: Please specify rounding control mechanism.
#endif

namespace boost {
namespace numeric {
namespace interval_lib {

/*
 * Three specializations of rounded_math<T>
 */

template<>
struct rounded_math<float>
  : save_state<rounded_arith_opp<float> >
{};

template<>
struct rounded_math<double>
  : save_state<rounded_arith_opp<double> >
{};

template<>
struct rounded_math<long double>
  : save_state<rounded_arith_opp<long double> >
{};

} // namespace interval_lib
} // namespace numeric
} // namespace boost

#endif // BOOST_NUMERIC_INTERVAL_HW_ROUNDING_HPP
