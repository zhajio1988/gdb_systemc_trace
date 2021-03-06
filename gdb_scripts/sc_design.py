# coding=utf-8
# Created by ripopov
from __future__ import print_function

import gdb_hacks
import sc_trace
import stdlib_hacks


def is_sc_object(val_type):
    return gdb_hacks.is_type_compatible(val_type, "sc_core::sc_object")


def is_sc_module(val_type):
    return gdb_hacks.is_type_compatible(val_type, "sc_core::sc_module")


def __is_module_or_interface(mtype):
    tname = mtype.strip_typedefs().name
    return tname in ("sc_core::sc_module", "sc_core::sc_interface")


def __get_plain_data_fields_rec(mtype, res):
    for field in mtype.fields():
        if field.is_base_class:
            if not __is_module_or_interface(field.type):
                __get_plain_data_fields_rec(field.type, res)
        elif not field.artificial:
            if not is_sc_object(field.type):
                res.append(field)

    return res


def get_plain_data_fields(mtype):
    res = []
    __get_plain_data_fields_rec(mtype, res)
    return res


class SCModuleMember(object):
    def __init__(self, val, name):
        self.value = val
        self.name = name

    def basename(self):
        return str(self.name).split('.')[-1]


class SCModule(object):

    def __init__(self, gdb_value):
        self.child_modules = []
        self.members = []
        self.name = ""
        self.value = gdb_value.cast(gdb_value.dynamic_type.strip_typedefs())

        if gdb_value.type.name == 'sc_core::sc_simcontext':
            self.__init_from_simctx()
        elif is_sc_module(gdb_value.type):
            self.__init_from_sc_module()
        else:
            assert False

    def __init_from_simctx(self):
        m_child_objects = stdlib_hacks.StdVectorView(self.value['m_child_objects'])
        self.name = "SYSTEMC_ROOT"

        for child_ptr in m_child_objects:
            child = child_ptr.dereference()
            child = child.cast(child.dynamic_type.strip_typedefs())

            if is_sc_module(child.type):
                self.child_modules.append(SCModule(child))
            else:
                self.members.append(SCModuleMember(child, str(child['m_name'])[1:-1]))

    def __init_from_sc_module(self):
        self.name = str(self.value['m_name'])[1:-1]

        m_child_objects_vec = stdlib_hacks.StdVectorView(self.value['m_child_objects'])

        for child_ptr in m_child_objects_vec:
            child = child_ptr.dereference()
            child = child.cast(child.dynamic_type)

            if is_sc_module(child.dynamic_type):
                self.child_modules.append(SCModule(child))
            else:
                self.members.append(SCModuleMember(child, str(child['m_name'])[1:-1]))

        for field in get_plain_data_fields(self.value.type):
            self.members.append(SCModuleMember(self.value[field.name], self.name + "." + field.name))

    def basename(self):
        return str(self.name).split('.')[-1]

    def __to_string(self, prefix):
        res = self.basename() + '    (' + str(self.value.dynamic_type.name) + ')'

        n_child_mods = len(self.child_modules)

        member_prefix = "│" if n_child_mods else " "

        for member in self.members:

            icon = " ○ "
            if is_sc_object(member.value.type):
                icon = " ◘ "

            res += "\n" + prefix + member_prefix + icon + member.basename() + "    (" + str(
                member.value.type.name) + ")     "

        for ii in range(0, n_child_mods):

            pref0 = "├"
            pref1 = "│"

            if ii == n_child_mods - 1:
                pref0 = "└"
                pref1 = " "

            res += "\n" + prefix + pref0 + "──" + self.child_modules[ii].__to_string(prefix + pref1 + "  ")

        return res

    def __str__(self):
        return self.__to_string("")

    def print_members(self):
        for member in self.members:
            print (member.name)

        for child_mod in self.child_modules:
            child_mod.print_members()

    def trace_all_tf(self, tracer):
        for member in self.members:
            tracer.trace(member.value, member.name)

        for child_mod in self.child_modules:
            child_mod.trace_all_tf(tracer)

    def trace_all(self, trace_file_name):
        print ("tracing all members: ", trace_file_name)
        tf = sc_trace.SCTrace(trace_file_name)
        self.trace_all_tf(tf)

    def trace_signal_tf(self, tracer, signal_path):
        if len(signal_path) > 1:
            child_mod = [mod for mod in self.child_modules if mod.basename() == signal_path[0]]
            assert len(child_mod) == 1
            child_mod[0].trace_signal_tf(tracer, signal_path[1:])
        else:
            selected_members = [member for member in self.members if member.basename() == signal_path[0]]
            if len(selected_members) == 1:
                tracer.trace(selected_members[0].value, selected_members[0].name)

    def trace_signals(self, trace_file_name, signal_list):
        print ("tracing selected signals: ", trace_file_name)
        tf = sc_trace.SCTrace(trace_file_name)
        for signal_name in signal_list:
            signal_path = signal_name.strip().split('.')
            self.trace_signal_tf(tf, signal_path)