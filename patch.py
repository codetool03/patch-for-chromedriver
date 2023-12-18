import io
import re
def patch_exe(executable_path):
    """Patches the ChromeDriver binary"""
    def gen_js_whitespaces(match):
        return b"\n" * len(match.group())

    def gen_call_function_js_cache_name(match):
        rep_len = len(match.group()) - 3
        ran_len = random.randint(6, rep_len)
        bb = b"'" + bytes(str().join(random.choices(
            population=string.ascii_letters, k=ran_len
        )), 'ascii') + b"';" + (b"\n" * (rep_len - ran_len))
        return bb

    with io.open(executable_path, "r+b") as fh:
        file_bin = fh.read()
        file_bin = re.sub(
            b"window\\.cdc_[a-zA-Z0-9]{22}_"
            b"(Array|Promise|Symbol|Object|Proxy|JSON)"
            b" = window\\.(Array|Promise|Symbol|Object|Proxy|JSON);",
            gen_js_whitespaces,
            file_bin,
        )
        file_bin = re.sub(
            b"window\\.cdc_[a-zA-Z0-9]{22}_"
            b"(Array|Promise|Symbol|Object|Proxy|JSON) \\|\\|",
            gen_js_whitespaces,
            file_bin,
        )
        file_bin = re.sub(
            b"'\\$cdc_[a-zA-Z0-9]{22}_';",
            gen_call_function_js_cache_name,
            file_bin,
        )
        fh.seek(0)
        fh.write(file_bin)
    print("ok")
    return True
patch_exe(r"D:\chromedriver.exe")
