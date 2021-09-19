# -*- coding: utf-8 -*-
import re

"""
Method for detecting Chinese characters
Refer to: https://stackoverflow.com/questions/2718196/find-all-chinese-text-in-a-string-using-python-and-regex
"""
LHan = [[0x2E80, 0x2E99],    # Han # So  [26] CJK RADICAL REPEAT, CJK RADICAL RAP
        [0x2E9B, 0x2EF3],    # Han # So  [89] CJK RADICAL CHOKE, CJK RADICAL C-SIMPLIFIED TURTLE
        [0x2F00, 0x2FD5],    # Han # So [214] KANGXI RADICAL ONE, KANGXI RADICAL FLUTE
        0x3005,              # Han # Lm       IDEOGRAPHIC ITERATION MARK
        0x3007,              # Han # Nl       IDEOGRAPHIC NUMBER ZERO
        [0x3021, 0x3029],    # Han # Nl   [9] HANGZHOU NUMERAL ONE, HANGZHOU NUMERAL NINE
        [0x3038, 0x303A],    # Han # Nl   [3] HANGZHOU NUMERAL TEN, HANGZHOU NUMERAL THIRTY
        0x303B,              # Han # Lm       VERTICAL IDEOGRAPHIC ITERATION MARK
        [0x3400, 0x4DB5],    # Han # Lo [6582] CJK UNIFIED IDEOGRAPH-3400, CJK UNIFIED IDEOGRAPH-4DB5
        [0x4E00, 0x9FC3],    # Han # Lo [20932] CJK UNIFIED IDEOGRAPH-4E00, CJK UNIFIED IDEOGRAPH-9FC3
        [0xF900, 0xFA2D],    # Han # Lo [302] CJK COMPATIBILITY IDEOGRAPH-F900, CJK COMPATIBILITY IDEOGRAPH-FA2D
        [0xFA30, 0xFA6A],    # Han # Lo  [59] CJK COMPATIBILITY IDEOGRAPH-FA30, CJK COMPATIBILITY IDEOGRAPH-FA6A
        [0xFA70, 0xFAD9],    # Han # Lo [106] CJK COMPATIBILITY IDEOGRAPH-FA70, CJK COMPATIBILITY IDEOGRAPH-FAD9
        [0x20000, 0x2A6D6],  # Han # Lo [42711] CJK UNIFIED IDEOGRAPH-20000, CJK UNIFIED IDEOGRAPH-2A6D6
        [0x2F800, 0x2FA1D]]  # Han # Lo [542] CJK COMPATIBILITY IDEOGRAPH-2F800, CJK COMPATIBILITY IDEOGRAPH-2FA1D

def build_zh_re():
    L = []
    for i in LHan:
        if isinstance(i, list):
            f, t = i
            try: 
                f = chr(f)
                t = chr(t)
                L.append('%s-%s' % (f, t))
            except: 
                pass # A narrow python build, so can't use chars > 65535 without surrogate pairs!

        else:
            try:
                L.append(chr(i))
            except:
                pass

    RE = '[%s]' % ''.join(L)
    return re.compile(RE, re.UNICODE)

# Ideographic description characters
# ⿰ ⿱ ⿲ ⿳ ⿴ ⿵ ⿶ ⿷ ⿸ ⿹ ⿺ ⿻
def build_idc_re():
    RE = "[%s-%s]" % ("⿰", "⿻")
    return re.compile(RE)
    
cn_re = build_zh_re()
idc_re = build_idc_re()

def decompose(composition):
    if len(composition) > 1:
        res = {}
        i = 0
        parts_count = 0
        parts_max = None
        is_parts = False
        next_step = 1
        # for comp in composition:
        while i < len(composition):
            comp = composition[i]
            # If exceed parts length, reset parts
            if parts_max and parts_count >= parts_max:
                is_parts = False
                parts_count = 0
                parts_max = None
                next_step = 1
                
            if is_parts:
                part = None
                next_step = 1
                is_inner = re.findall(idc_re, comp)
                if is_inner:
                    inner_structure = is_inner[0]
                    inner_parts_max = 3 if inner_structure == '⿲' or inner_structure == '⿳' else 2
                    next_step = inner_parts_max + 1
                    part = decompose(composition[i:(i + next_step)])
                else:
                    part = comp
                
                if part:
                    res["children"].append(part)
                    parts_count += 1
            elif re.findall(idc_re, comp):
                res["structure"] = comp
                res["children"] = []
                parts_max = 3 if comp == '⿲' or comp == '⿳' else 2
                parts_count = 0
                next_step = 1
                is_parts = True
                
            i += next_step
        return res
    return None

test = decompose("⿰⿱匕矢⿱子止")
print(test)