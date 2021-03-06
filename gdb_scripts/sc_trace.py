# Created by ripopov
from __future__ import print_function

import gdb

import gdb_hacks
import stdlib_hacks


class SCTrace:
    def __init__(self, trace_file_name):
        self.sc_create_vcd_trace_file = gdb_hacks.lookup_global_function(
            'sc_core::sc_create_vcd_trace_file(char const*)')
        self.sc_close_vcd_trace_file = \
            gdb_hacks.lookup_global_function('sc_core::sc_close_vcd_trace_file(sc_core::sc_trace_file*)')

        self.sc_trace_char_ptr = gdb_hacks.lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, char const*, ' + stdlib_hacks.std_string_name + ' const&, int)')
        self.sc_trace_short_ptr = gdb_hacks.lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, short const*, ' + stdlib_hacks.std_string_name + ' const&, int)')
        self.sc_trace_int_ptr = gdb_hacks.lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, int const*, ' + stdlib_hacks.std_string_name + ' const&, int)')
        self.sc_trace_long_ptr = gdb_hacks.lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, long const*, ' + stdlib_hacks.std_string_name + ' const&, int)')
        self.sc_trace_long_long_ptr = gdb_hacks.lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, long long const*, ' + stdlib_hacks.std_string_name + ' const&, int)')

        self.sc_trace_unsigned_char_ptr = gdb_hacks.lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, unsigned char const*, ' + stdlib_hacks.std_string_name + ' const&, int)')
        self.sc_trace_unsigned_short_ptr = gdb_hacks.lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, unsigned short const*, ' + stdlib_hacks.std_string_name + ' const&, int)')
        self.sc_trace_unsigned_int_ptr = gdb_hacks.lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, unsigned int const*, ' + stdlib_hacks.std_string_name + ' const&, int)')
        self.sc_trace_unsigned_long_ptr = gdb_hacks.lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, unsigned long const*, ' + stdlib_hacks.std_string_name + ' const&, int)')
        self.sc_trace_unsigned_long_long_ptr = gdb_hacks.lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, unsigned long long const*, ' + stdlib_hacks.std_string_name + ' const&, int)')

        self.sc_trace_bool_ptr = gdb_hacks.lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, bool const*, ' + stdlib_hacks.std_string_name + ' const&)')
        self.sc_trace_float_ptr = gdb_hacks.lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, float const*, ' + stdlib_hacks.std_string_name + ' const&)')
        self.sc_trace_double_ptr = gdb_hacks.lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, double const*, ' + stdlib_hacks.std_string_name + ' const&)')

        self.sc_trace_sc_bit_ptr = gdb_hacks.lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, sc_dt::sc_bit const*, ' + stdlib_hacks.std_string_name + ' const&)')
        self.sc_trace_sc_logic_ptr = gdb_hacks.lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, sc_dt::sc_logic const*, ' + stdlib_hacks.std_string_name + ' const&)')
        self.sc_trace_sc_int_base_ptr = gdb_hacks.lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, sc_dt::sc_int_base const*, ' + stdlib_hacks.std_string_name + ' const&)')
        self.sc_trace_sc_uint_base_ptr = gdb_hacks.lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, sc_dt::sc_uint_base const*, ' + stdlib_hacks.std_string_name + ' const&)')
        self.sc_trace_sc_signed_ptr = gdb_hacks.lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, sc_dt::sc_signed const*, ' + stdlib_hacks.std_string_name + ' const&)')
        self.sc_trace_sc_unsigned_ptr = gdb_hacks.lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, sc_dt::sc_unsigned const*, ' + stdlib_hacks.std_string_name + ' const&)')

        self.sc_trace_sc_bv_base_ptr = gdb_hacks.lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, sc_dt::sc_bv_base const*, ' + stdlib_hacks.std_string_name + ' const&)')
        self.sc_trace_sc_lv_base_ptr = gdb_hacks.lookup_global_function(
            'sc_core::sc_trace(sc_core::sc_trace_file*, sc_dt::sc_lv_base const*, ' + stdlib_hacks.std_string_name + ' const&)')

        self.tf = self.sc_create_vcd_trace_file(trace_file_name)

    def trace(self, gdb_value, name):
        real_type = gdb_value.type.strip_typedefs()

        size_bit = 8 * real_type.sizeof

        if real_type.name and gdb_value.address:
            if real_type.name == "char":
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_char_ptr(self.tf, gdb_value.address, name_str, size_bit)

            elif real_type.name == "signed char":
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_char_ptr(self.tf, gdb_value.address, name_str, size_bit)

            elif real_type.name == "short":
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_short_ptr(self.tf, gdb_value.address, name_str, size_bit)

            elif real_type.name == "int":
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_int_ptr(self.tf, gdb_value.address, name_str, size_bit)

            elif real_type.name == "long":
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_long_ptr(self.tf, gdb_value.address, name_str, size_bit)

            elif real_type.name == "long long":
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_long_long_ptr(self.tf, gdb_value.address, name_str, size_bit)

            elif real_type.name == "unsigned char":
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_unsigned_char_ptr(self.tf, gdb_value.address, name_str, size_bit)

            elif real_type.name == "unsigned short":
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_unsigned_short_ptr(self.tf, gdb_value.address, name_str, size_bit)

            elif real_type.name == "unsigned int":
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_unsigned_int_ptr(self.tf, gdb_value.address, name_str, size_bit)

            elif real_type.name == "unsigned long":
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_unsigned_long_ptr(self.tf, gdb_value.address, name_str, size_bit)

            elif real_type.name == "unsigned long long":
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_unsigned_long_long_ptr(self.tf, gdb_value.address, name_str, size_bit)

            elif real_type.name == "bool":
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_bool_ptr(self.tf, gdb_value.address, name_str)

            elif real_type.name == "float":
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_float_ptr(self.tf, gdb_value.address, name_str)

            elif real_type.name == "double":
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_double_ptr(self.tf, gdb_value.address, name_str)

            elif gdb_hacks.is_type_compatible(real_type, "sc_dt::sc_bit"):
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_sc_bit_ptr(self.tf, gdb_value.address, name_str)

            elif gdb_hacks.is_type_compatible(real_type, "sc_dt::sc_logic"):
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_sc_logic_ptr(self.tf, gdb_value.address, name_str)

            elif gdb_hacks.is_type_compatible(real_type, "sc_dt::sc_int_base"):
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_sc_int_base_ptr(self.tf, gdb_value.address, name_str)

            elif gdb_hacks.is_type_compatible(real_type, "sc_dt::sc_uint_base"):
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_sc_uint_base_ptr(self.tf, gdb_value.address, name_str)

            elif gdb_hacks.is_type_compatible(real_type, "sc_dt::sc_signed"):
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_sc_signed_ptr(self.tf, gdb_value.address, name_str)

            elif gdb_hacks.is_type_compatible(real_type, "sc_dt::sc_unsigned"):
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_sc_unsigned_ptr(self.tf, gdb_value.address, name_str)

            elif gdb_hacks.is_type_compatible(real_type, "sc_dt::sc_bv_base"):
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_sc_bv_base_ptr(self.tf, gdb_value.address, name_str)

            elif gdb_hacks.is_type_compatible(real_type, "sc_dt::sc_lv_base"):
                name_str = stdlib_hacks.create_std_string(name)
                self.sc_trace_sc_lv_base_ptr(self.tf, gdb_value.address, name_str)

            elif real_type.name == "sc_core::sc_clock" or real_type.name.startswith("sc_core::sc_signal<"):
                m_cur_val = gdb_value['m_cur_val']
                self.trace(m_cur_val, name)

            elif gdb_hacks.is_type_compatible(real_type, "sc_core::sc_method_process"):
                pass

            elif gdb_hacks.is_type_compatible(real_type, "sc_core::sc_thread_process"):
                pass

            elif real_type.name.startswith("sc_core::sc_in<") or real_type.name.startswith("sc_core::sc_out<"):
                m_interface = gdb_value['m_interface']
                m_interface = m_interface.reinterpret_cast(m_interface.dynamic_type)
                sig_val = m_interface.dereference()
                self.trace(sig_val, name)

            elif real_type.name.startswith("sc_core::sc_in<") or real_type.name.startswith("sc_core::sc_out<"):
                m_interface = gdb_value['m_interface']
                m_interface = m_interface.reinterpret_cast(m_interface.dynamic_type)
                sig_val = m_interface.dereference()
                self.trace(sig_val, name)

            elif real_type.code == gdb.TYPE_CODE_STRUCT and not real_type.name.startswith("sc_core::") \
                    and not real_type.name.startswith("sc_dt::") and not real_type.name.startswith("std::"):
                for member in gdb_hacks.get_data_member_list(gdb_value):
                    self.trace(member[0], name + "*" + member[1])

            else:
                # print ("Type not supported yet: " + real_type.name)
                pass
