"""Exception handling

Just a stub for now.

"""
import sys
import traceback


def maybe_print(obj):
    for key in dir(obj):
        if key.startswith("__"):
            continue
        try:
            value = getattr(obj, key)
            if len(repr(value)) > 75:
                value = repr(value[0:70]) + " ..."
            print(key, value)
        except:
            print("couldn't print", key)


def avantpy_excepthook(type, value, tb):
    print("type = ", type)
    print("value = ", value)
    print("\n=======================================")
    for lineno, line in enumerate(traceback.format_exception(type, value, tb)):
        print(lineno, ":", line)

    # while tb:
    #     print("\n=======================================")
    #     print("filename = ", tb.tb_frame.f_code.co_filename)
    #     print("name ", tb.tb_frame.f_code.co_name)
    #     print("lineno = ", tb.tb_lineno)
    #     # print("\ntb:")
    #     # maybe_print(tb)
    #     # print("\n------------")
    #     # print("tb_frame:")
    #     # maybe_print(tb.tb_frame)
    #     # print('\ntb_frame.f_code:')
    #     # maybe_print(tb.tb_frame.f_code)
    #     # break
    #     tb = tb.tb_next


def activate():
    sys.excepthook = avantpy_excepthook
