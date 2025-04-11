
# WARNING: THIS FILE IS AUTO-GENERATED. DO NOT MODIFY.

# This file was generated from auto_ctrl.idl
# using RTI Code Generator (rtiddsgen) version 4.3.0.
# The rtiddsgen tool is part of the RTI Connext DDS distribution.
# For more information, type 'rtiddsgen -help' at a command shell
# or consult the Code Generator User's Manual.

from dataclasses import field
from typing import Union, Sequence, Optional
import rti.idl as idl
from enum import IntEnum
import sys
import os


@idl.struct(
    member_annotations = {
        'object_dist': [idl.array([5])],
    }
)
class auto_ctl:
    auto_enable: bool = False
    heading_error: idl.float32 = 0.0
    object_dist: Sequence[idl.float32] = field(default_factory = idl.array_factory(idl.float32, [5]))
    obstacle_flag: bool = False
